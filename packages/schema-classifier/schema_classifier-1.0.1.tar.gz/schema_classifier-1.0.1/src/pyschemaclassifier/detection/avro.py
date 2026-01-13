
"""Avro schema-only extractor + meta"""
from typing import Dict, Any
import os, re

from fastavro import reader

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

def _avro_type_to_spark(t: Any) -> str:
    if isinstance(t,str):
        return {'int':'integer','long':'integer','float':'double','double':'double','boolean':'boolean','bytes':'binary','string':'string'}.get(t,'string')
    if isinstance(t,dict):
        lt=t.get('logicalType')
        if lt=='decimal':
            p=t.get('precision',38); s=t.get('scale',18); return f'decimal({p},{s})'
        if lt=='date': return 'date'
        if lt in ('timestamp-millis','timestamp-micros'): return 'timestamp'
        return _avro_type_to_spark(t.get('type','string'))
    if isinstance(t,list): return 'string'
    return 'string'

def extract(path: str) -> Dict[str, Any]:
    try:
        with open(path,'rb') as fo:
            r=reader(fo); schema=r.schema
    except Exception:
        regex,pattern=_build_regex_and_pattern(os.path.basename(path))
        return {"type":"struct","fields":[], "meta": {"file_name": os.path.basename(path), "file_name_regex": regex, "file_name_pattern": pattern}}
    fields=[]
    for f in schema.get('fields',[]):
        fields.append({'name': f.get('name'), 'type': _avro_type_to_spark(f.get('type')), 'nullable': True, 'metadata': {}})
    regex,pattern=_build_regex_and_pattern(os.path.basename(path))
    return {"type":"struct","fields":fields, "meta": {"file_name": os.path.basename(path), "file_name_regex": regex, "file_name_pattern": pattern}}
