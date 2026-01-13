
"""ORC schema extractor + meta (optional pyorc)"""
from typing import Dict, Any
import os, re

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

def extract(path: str) -> Dict[str, Any]:
    try:
        import pyorc
    except Exception:
        regex,pattern=_build_regex_and_pattern(os.path.basename(path))
        return {"type":"struct","fields":[], "meta": {"file_name": os.path.basename(path), "file_name_regex": regex, "file_name_pattern": pattern}, "warnings": ["pyorc not available; install with pip install -e .[orc]"]}
    fields=[]
    try:
        with open(path,'rb') as fo:
            r=pyorc.Reader(fo)
            for name,col in r.schema.fields.items():
                kind=getattr(col,'kind','string')
                m={'int':'integer','long':'integer','short':'integer','byte':'integer','float':'double','double':'double','boolean':'boolean','string':'string','binary':'binary','timestamp':'timestamp','date':'date'}
                fields.append({'name': name, 'type': m.get(str(kind),'string'), 'nullable': True, 'metadata': {}})
    except Exception:
        regex,pattern=_build_regex_and_pattern(os.path.basename(path))
        return {"type":"struct","fields":[], "meta": {"file_name": os.path.basename(path), "file_name_regex": regex, "file_name_pattern": pattern}}
    regex,pattern=_build_regex_and_pattern(os.path.basename(path))
    return {"type":"struct","fields":fields, "meta": {"file_name": os.path.basename(path), "file_name_regex": regex, "file_name_pattern": pattern}}
