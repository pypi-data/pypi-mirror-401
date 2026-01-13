
"""XML minimal detector with BOM + meta"""
from typing import List, Dict, Any
import os, re
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

def _infer_primitive(values: List[str]) -> str:
    seen=[v for v in values if v and str(v).strip()!='']
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


def detect(path: str) -> Dict[str, Any]:
    try:
        import xml.etree.ElementTree as ET
        text = open(path, 'r', encoding='utf-8').read()
        text = text.lstrip('\ufeff')  # BOM strip
        root = ET.fromstring(text)
    except Exception:
        regex, pattern = _build_regex_and_pattern(os.path.basename(path))
        return {
            "type": "struct",
            "fields": [],
            "meta": {
                "file_name": os.path.basename(path),
                "file_name_regex": regex,
                "file_name_pattern": pattern
            }
        }

    children = list(root)
    from collections import defaultdict
    groups = defaultdict(list)
    for c in children:
        groups[c.tag].append(c)

    fields = []
    for tag, elems in groups.items():
        if len(elems) > 1:
            # array<object> and surface nested child fields from the first element
            sample = elems[0]
            child_names = []
            # include element text nodes (if meaningful) and attributes
            # but here we focus on sub-elements as columns
            nested = list(sample)
            child_fields_meta = []
            for ch in nested:
                vals = []
                if ch.text:
                    vals.append(ch.text)
                # attributes can be treated as additional columns:
                for k, v in ch.attrib.items():
                    vals.append(v)
                t = _infer_primitive(vals)
                # nullable false if sample had text; in full MVP we’d compute across all elems
                child_fields_meta.append({
                    "name": ch.tag,
                    "type": t,
                    "nullable": False
                })

            fields.append({
                "name": tag,
                "type": "array<object>",
                "nullable": False,
                "metadata": {
                    "child_fields": child_fields_meta
                }
            })
        else:
            # single child element → primitive from text/attributes
            vals = []
            e = elems[0]
            if e.text:
                vals.append(e.text)
            for k, v in e.attrib.items():
                vals.append(v)
            t = _infer_primitive(vals)
            fields.append({
                "name": tag,
                "type": t,
                "nullable": True,
                "metadata": {}
            })

    regex, pattern = _build_regex_and_pattern(os.path.basename(path))
    return {
        "type": "struct",
        "fields": fields,
        "meta": {
            "file_name": os.path.basename(path),
            "file_name_regex": regex,
            "file_name_pattern": pattern
        }
    }
