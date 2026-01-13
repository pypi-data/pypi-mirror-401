
"""Hudi minimal extractor (COW) via Parquet + meta"""
from typing import Dict, Any
import os, re, glob
from . import parquet as parquet_detector

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
    hoodie=os.path.join(base_path,'.hoodie')
    fields=[]
    if os.path.isdir(hoodie):
        ps=glob.glob(os.path.join(base_path,'**','*.parquet'), recursive=True)
        if ps:
            res=parquet_detector.extract(ps[0])
            fields=res.get('fields',[])
    regex,pattern=_build_regex_and_pattern(_basename(base_path))
    return {"type":"struct","fields":fields, "meta": {"file_name": _basename(base_path), "file_name_regex": regex, "file_name_pattern": pattern}}
