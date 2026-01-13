"""Parquet footer-only extractor + meta"""
from typing import Dict, Any
import os
import pyarrow.parquet as pq
import pyarrow as pa
import re

import os as _os
import re as _re

def _build_regex_and_pattern(name: str):
    escaped = _re.escape(name)
    digit_runs = [(m.start(), m.end()) for m in _re.finditer(r"\d+", name)]
    if not digit_runs:
        return '^' + escaped + '$', name
    longest = max(digit_runs, key=lambda t: (t[1]-t[0], -t[0]))
    start, end = longest
    pre = name[:start]
    post = name[end:]
    regex = '^' + _re.escape(pre) + r"\d{" + str(end-start) + '}' + _re.escape(post) + '$'
    pattern = pre + '*' + post
    return regex, pattern

def _arrow_to_spark_type(t) -> str:
    if pa.types.is_int8(t) or pa.types.is_int16(t) or pa.types.is_int32(t) or pa.types.is_int64(t): return 'integer'
    if pa.types.is_float16(t) or pa.types.is_float32(t) or pa.types.is_float64(t): return 'double'
    if pa.types.is_boolean(t): return 'boolean'
    if pa.types.is_binary(t) or pa.types.is_large_binary(t): return 'binary'
    if pa.types.is_string(t) or pa.types.is_large_string(t): return 'string'
    if pa.types.is_timestamp(t): return 'timestamp'
    if pa.types.is_date(t): return 'date'
    if pa.types.is_decimal(t): return f"decimal({t.precision},{t.scale})"
    if pa.types.is_list(t): return f"array<{_arrow_to_spark_type(t.value_type)}>"
    if pa.types.is_struct(t): return 'object'
    return 'string'

def extract(path: str) -> Dict[str, Any]:
    try:
        schema=pq.read_schema(path)
    except Exception:
        regex,pattern=_build_regex_and_pattern(os.path.basename(path))
        return {"type":"struct","fields":[], "meta": {"file_name": os.path.basename(path), "file_name_regex": regex, "file_name_pattern": pattern}}
    fields=[]
    for field in schema:
        fields.append({"name": field.name, "type": _arrow_to_spark_type(field.type), "nullable": field.nullable, "metadata": {}})
    regex,pattern=_build_regex_and_pattern(os.path.basename(path))
    return {"type":"struct","fields":fields, "meta": {"file_name": os.path.basename(path), "file_name_regex": regex, "file_name_pattern": pattern}}
