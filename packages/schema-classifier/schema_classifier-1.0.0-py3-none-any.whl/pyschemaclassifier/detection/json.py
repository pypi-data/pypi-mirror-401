
"""JSON/NDJSON minimal detector with BOM + meta"""
from typing import List, Dict, Any
import json, os, re
from datetime import datetime

import os, re

def _basename(path: str) -> str:
    return os.path.basename(os.path.normpath(path))

def _build_regex_and_pattern(name: str):
    escaped = re.escape(name)
    digit_runs = [(m.start(), m.end()) for m in re.finditer(r"\d+", name)]
    if not digit_runs:
        return '^' + escaped + '$', name
    longest = max(digit_runs, key=lambda t: (t[1]-t[0], -t[0]))
    start, end = longest
    pre = name[:start]
    post = name[end:]
    regex = '^' + re.escape(pre) + r"\d{" + str(end-start) + '}' + re.escape(post) + '$'
    pattern = pre + '*' + post
    return regex, pattern

NUMERIC_INT_RE = re.compile(r"^[+-]?\d+$")
NUMERIC_FLOAT_RE = re.compile(r"^[+-]?(?:\d+\.\d*|\d*\.\d+)(?:[eE][+-]?\d+)?$|^[+-]?\d+(?:[eE][+-]?\d+)$")
BOOLEAN_SET_TRUE = {"true","t","yes","y","1"}
BOOLEAN_SET_FALSE = {"false","f","no","n","0"}
DATE_PATTERNS=["%Y-%m-%d"]; TS_PATTERNS=["%Y-%m-%d %H:%M:%S"]

def _strip_bom(text: str) -> str:
    return text.lstrip('﻿') if text.startswith('﻿') else text

def _infer_primitive(values: List[Any]) -> str:
    seen=[v for v in values if v is not None and str(v).strip()!='']
    if not seen: return 'string'
    b=[str(v).strip().lower() for v in seen]
    if all(x in BOOLEAN_SET_TRUE|BOOLEAN_SET_FALSE for x in b): return 'boolean'
    if all(NUMERIC_INT_RE.match(str(v).strip()) for v in seen):
        if any(len(str(v).strip().lstrip('+-'))>18 for v in seen): return 'string'
        if any(str(v).strip().lstrip('+-').startswith('0') and len(str(v).strip().lstrip('+-'))>1 for v in seen): return 'string'
        return 'integer'
    if all(NUMERIC_INT_RE.match(str(v).strip()) or NUMERIC_FLOAT_RE.match(str(v).strip()) for v in seen): return 'double'
    try:
        if all(datetime.strptime(str(v).strip(), DATE_PATTERNS[0]) for v in seen): return 'date'
    except Exception: pass
    try:
        if all(datetime.strptime(str(v).strip(), TS_PATTERNS[0]) for v in seen): return 'timestamp'
    except Exception: pass
    return 'string'

def _schema_from_object_samples(samples: List[Dict[str, Any]]):
    keys=[]; seen=set()
    for obj in samples:
        for k in obj.keys():
            if k not in seen:
                keys.append(k); seen.add(k)
    fields=[]
    for k in keys:
        vals=[s.get(k) for s in samples]
        if any(isinstance(v, dict) for v in vals if v is not None): t='object'
        elif any(isinstance(v, list) for v in vals if v is not None):
            elem=[]
            for v in vals:
                if isinstance(v,list): elem.extend(v[:10])
            et=_infer_primitive(elem) if elem else 'string'; t=f'array<{et}>'
        else:
            t=_infer_primitive(vals)
        nullable=any((v is None) or (str(v).strip()=="") or (k not in s) for s,v in zip(samples,vals))
        fields.append({"name":k,"type":t,"nullable":nullable,"metadata":{}})
    return fields

def detect(path: str, sample_records: int=500) -> Dict[str, Any]:
    # Try NDJSON
    nd=[]; parsed=0; total=0
    try:
        with open(path,'r',encoding='utf-8') as f:
            for i,line in enumerate(f):
                if i==0: line=_strip_bom(line)
                s=line.strip(); 
                if not s: 
                    continue
                total+=1
                try:
                    obj=json.loads(s); nd.append(obj); parsed+=1
                except Exception: pass
                if len(nd)>=sample_records: break
    except Exception: nd=[]
    if nd and total>0 and (parsed/max(1,total))>=0.95 and all(isinstance(x,(dict,list)) for x in nd):
        objs=[x for x in nd if isinstance(x,dict)]; arrs=[x for x in nd if isinstance(x,list)]
        fields=[]
        if objs: fields.extend(_schema_from_object_samples(objs))
        if arrs:
            elem=[]
            for a in arrs: elem.extend(a[:10])
            et=_infer_primitive(elem) if elem else 'string'
            fields.append({"name":"value","type":f"array<{et}>","nullable":False,"metadata":{}})
        regex,pattern=_build_regex_and_pattern(os.path.basename(path))
        return {"type":"struct","fields":fields, "meta": {"file_name": os.path.basename(path), "file_name_regex": regex, "file_name_pattern": pattern}}
    # Single JSON
    try:
        text=_strip_bom(open(path,'r',encoding='utf-8').read()); data=json.loads(text)
    except Exception:
        regex,pattern=_build_regex_and_pattern(os.path.basename(path))
        return {"type":"struct","fields":[], "meta": {"file_name": os.path.basename(path), "file_name_regex": regex, "file_name_pattern": pattern}}
    if isinstance(data, dict): fields=_schema_from_object_samples([data]); schema={"type":"struct","fields":fields}
    elif isinstance(data, list):
        objs=[x for x in data[:sample_records] if isinstance(x,dict)]
        if objs:
            fields=_schema_from_object_samples(objs); schema={"type":"struct","fields":fields}
        else:
            et=_infer_primitive(data[:sample_records]); schema={"type":"struct","fields":[{"name":"value","type":f"array<{et}>","nullable":False,"metadata":{}}]}
    else:
        t=_infer_primitive([data]); schema={"type":"struct","fields":[{"name":"value","type":t,"nullable":False,"metadata":{}}]}
    regex,pattern=_build_regex_and_pattern(os.path.basename(path))
    schema["meta"]={"file_name": os.path.basename(path), "file_name_regex": regex, "file_name_pattern": pattern}
    return schema
