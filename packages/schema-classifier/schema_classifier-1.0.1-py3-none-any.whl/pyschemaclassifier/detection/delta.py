
"""Delta minimal extractor from _delta_log schemaString + meta"""
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
    log_dir=os.path.join(base_path,'_delta_log')
    fields=[]
    if os.path.isdir(log_dir):
        files=[f for f in os.listdir(log_dir) if f.endswith('.json')]
        if files:
            def keyf(fn):
                nums=re.findall(r"\d+", fn)
                return int(nums[0]) if nums else 0
            latest=max(files, key=keyf)
            try:
                for line in open(os.path.join(log_dir, latest),'r',encoding='utf-8'):
                    try:
                        rec=json.loads(line.strip())
                    except Exception:
                        continue
                    if 'metaData' in rec:
                        s=rec['metaData'].get('schemaString')
                        if s:
                            try:
                                sj=json.loads(s)
                                for f in sj.get('fields',[]):
                                    fields.append({'name': f.get('name'), 'type': f.get('type') if isinstance(f.get('type'),str) else 'object', 'nullable': f.get('nullable', True), 'metadata': f.get('metadata', {})})
                                break
                            except Exception:
                                pass
            except Exception:
                pass
    regex,pattern=_build_regex_and_pattern(_basename(base_path))
    return {"type":"struct","fields":fields, "meta": {"file_name": _basename(base_path), "file_name_regex": regex, "file_name_pattern": pattern}}
