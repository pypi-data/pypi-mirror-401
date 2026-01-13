
"""Iceberg minimal extractor from metadata.json + meta"""
from typing import Dict, Any
import os, re, json

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

def extract_table_schema(base_path: str) -> Dict[str, Any]:
    meta=os.path.join(base_path,'metadata.json')
    fields=[]
    if os.path.isfile(meta):
        try:
            m=json.load(open(meta,'r',encoding='utf-8'))
            curr=m.get('current-schema-id'); schema_obj=None
            if isinstance(m.get('schemas'),list):
                for s in m['schemas']:
                    if s.get('schema-id')==curr:
                        schema_obj=s; break
                if schema_obj is None and m['schemas']:
                    schema_obj=m['schemas'][0]
            elif 'schema' in m:
                schema_obj=m['schema']
            if schema_obj and 'fields' in schema_obj:
                for f in schema_obj['fields']:
                    name=f.get('name'); t=f.get('type')
                    tname='string'
                    if isinstance(t,str):
                        tname={'int':'integer','long':'integer','float':'double','double':'double','boolean':'boolean','string':'string','binary':'binary','date':'date','timestamp':'timestamp'}.get(t,'string')
                    elif isinstance(t,dict):
                        if t.get('type')=='decimal':
                            p=t.get('precision',38); s=t.get('scale',18); tname=f'decimal({p},{s})'
                        elif t.get('type')=='list':
                            elem=t.get('element','string'); tname=f'array<{elem if isinstance(elem,str) else "string"}>'
                        elif t.get('type')=='struct': tname='object'
                    fields.append({'name': name, 'type': tname, 'nullable': True, 'metadata': {}})
        except Exception:
            pass
    regex,pattern=_build_regex_and_pattern(_basename(base_path))
    return {"type":"struct","fields":fields, "meta": {"file_name": _basename(base_path), "file_name_regex": regex, "file_name_pattern": pattern}}
