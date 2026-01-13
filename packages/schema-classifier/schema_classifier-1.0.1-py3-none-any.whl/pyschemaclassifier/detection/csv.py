
"""CSV minimal detector with BOM + meta"""
from typing import List, Dict, Any, Optional
import csv, re, os
from datetime import datetime

BOOLEAN_SET_TRUE = {"true","t","yes","y","1"}
BOOLEAN_SET_FALSE = {"false","f","no","n","0"}
DATE_PATTERNS = ["%Y-%m-%d"]
TS_PATTERNS = ["%Y-%m-%d %H:%M:%S"]
NUMERIC_INT_RE = re.compile(r"^[+-]?\d+$")
NUMERIC_FLOAT_RE = re.compile(r"^[+-]?(?:\d+\.\d*|\d*\.\d+)(?:[eE][+-]?\d+)?$|^[+-]?\d+(?:[eE][+-]?\d+)$")


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


def _strip_bom_first(row: List[str]) -> List[str]:
    if row and row[0].startswith('﻿'):
        row[0] = row[0].replace('﻿','')
    return row

def _infer_type(values: List[str]) -> str:
    seen = [v for v in values if v and v.strip() != '']
    if not seen: return 'string'
    if all(v.lower() in BOOLEAN_SET_TRUE|BOOLEAN_SET_FALSE for v in seen): return 'boolean'
    if all(NUMERIC_INT_RE.match(v.strip()) for v in seen):
        if any(len(v.strip().lstrip('+-'))>18 for v in seen): return 'string'
        if any(v.strip().lstrip('+-').startswith('0') and len(v.strip().lstrip('+-'))>1 for v in seen): return 'string'
        return 'integer'
    if all(NUMERIC_INT_RE.match(v.strip()) or NUMERIC_FLOAT_RE.match(v.strip()) for v in seen): return 'double'
    if all(_try_date(v) for v in seen): return 'date'
    if all(_try_ts(v) for v in seen): return 'timestamp'
    return 'string'

def _try_date(v: str) -> bool:
    try:
        datetime.strptime(v.strip(), DATE_PATTERNS[0]); return True
    except Exception: return False

def _try_ts(v: str) -> bool:
    try:
        datetime.strptime(v.strip(), TS_PATTERNS[0]); return True
    except Exception: return False

def detect(path: str, delimiter: Optional[str]=None, header_mode: str='auto', sample_records: int=500) -> Dict[str, Any]:
    delim = delimiter or ','
    rows: List[List[str]] = []
    with open(path,'r',encoding='utf-8') as f:
        r = csv.reader(f, delimiter=delim, quotechar='"', escapechar='\\')
        for i,row in enumerate(r):
            if i==0: row = _strip_bom_first(row)
            rows.append(row)
            if i+1>=sample_records: break
    if not rows: return {"type":"struct","fields":[]}
    first = rows[0]
    header=False
    if header_mode=='true': header=True
    elif header_mode=='false': header=False
    else:
        alpha_count = sum(1 for v in first if re.search(r"[A-Za-z_]", v or ""))
        header = (alpha_count/max(1,len(first)))>=0.80
    data = rows[1:] if header else rows
    from collections import Counter
    col_count = Counter(len(r) for r in data if r).most_common(1)[0][0] if data else len(first)
    cols = [[] for _ in range(col_count)]
    for r in data:
        if len(r)!=col_count: continue
        for j,v in enumerate(r): cols[j].append(v)
    names = [ (first[j] if header and j<len(first) and first[j] else f"col{j}") for j in range(col_count) ]
    fields=[]
    for j in range(col_count):
        t=_infer_type(cols[j]); nullable=any((v is None) or (str(v).strip()=="") for v in cols[j])
        fields.append({"name":names[j],"type":t,"nullable":nullable,"metadata":{}})
    regex, pattern = _build_regex_and_pattern(os.path.basename(path))
    return {"type":"struct","fields":fields, "meta": {"file_name": os.path.basename(path), "file_name_regex": regex, "file_name_pattern": pattern}}
