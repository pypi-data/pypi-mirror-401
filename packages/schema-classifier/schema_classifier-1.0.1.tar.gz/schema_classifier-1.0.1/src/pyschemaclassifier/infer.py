
"""Orchestrator (CSV+JSON+XML+Parquet+Avro+ORC+Delta/Iceberg/Hudi) with dir mode and detection_mode wiring"""
from typing import Optional, Dict, Any, List
import os
import pandas as pd
from pyspark.sql import DataFrame as _SparkDF

from .exceptions import DetectionError
from .detection import csv as csv_detector
from .detection import json as json_detector
from .detection import parquet as parquet_detector
from .detection import xml as xml_detector
from .detection import avro as avro_detector
from .detection import orc as orc_detector
from .detection import delta as delta_detector
from .detection import iceberg as iceberg_detector
from .detection import hudi as hudi_detector
from .detection import classifier as cls

SUPPORTED_EXTS = {'.csv','.tsv','.ndjson','.json','.xml','.parquet','.avro','.orc'}

# Simple extension -> format mapping
EXT_FMT_MAP = {
    '.csv': 'csv', '.tsv': 'csv', '.json': 'json', '.ndjson': 'ndjson',
    '.xml': 'xml', '.parquet': 'parquet', '.avro': 'avro', '.orc': 'orc'
}


def detect_schema(input_path: Optional[str]=None, spark_df: Optional[Any]=None, pandas_df: Optional[Any]=None,
                  detection_mode: str='trust_hint', coverage_mode: str='max', sample_records: int=500,
                  csv_header: str='auto', csv_delimiter: str=None, **kwargs) -> Dict[str, Any]:
    sources=[input_path, spark_df, pandas_df]
    if sum(1 for s in sources if s is not None)!=1:
        raise DetectionError('Provide exactly one source: input_path OR spark_df OR pandas_df.')

    if spark_df is not None:
        if not isinstance(spark_df, _SparkDF):
            raise TypeError(f"Expected a Spark DataFrame for 'spark_df', got: {type(spark_df)!r}")

        from .dataframe.spark import detect_schema_from_df as _spark_detect
        schema = _spark_detect(spark_df)
        return schema

    if pandas_df is not None:
        if not isinstance(pandas_df, pd.DataFrame):
            raise TypeError(f"Expected a pandas DataFrame for 'pandas_df', got: {type(pandas_df)!r}")

        from .dataframe.pandas import detect_schema_from_df as _pandas_detect
        schema = _pandas_detect(pandas_df)
        return schema

    if input_path:
        input_path=os.path.normpath(input_path)
        
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input path does not exist: {input_path}")

        if os.path.isdir(input_path):
            # Table formats
            delta_log=os.path.join(input_path,'_delta_log'); iceberg_meta=os.path.join(input_path,'metadata.json'); hudi_marker=os.path.join(input_path,'.hoodie')
            if os.path.isdir(delta_log): return delta_detector.extract_table_schema(input_path)
            if os.path.isfile(iceberg_meta): return iceberg_detector.extract_table_schema(input_path)
            if os.path.isdir(hudi_marker): return hudi_detector.extract_table_schema(input_path)

            files=[f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path,f))]
            results=[]
            for fname in files:
                ext=os.path.splitext(fname)[1].lower()
                if ext not in SUPPORTED_EXTS: continue
                fpath=os.path.join(input_path,fname)
                item=_detect_single_file(fpath, sample_records, csv_header, csv_delimiter, detection_mode)
                results.append(item)
                if coverage_mode=='any' and item.get('fields'):
                    # Stop after first successful detection in 'any' mode
                    break
            return {"type":"struct","fields":[],"files":results}
        else:
            return _detect_single_file(input_path, sample_records, csv_header, csv_delimiter, detection_mode)

    return {"type":"struct","fields":[]}


def _detect_single_file(path: str, sample_records: int, csv_header: str, csv_delimiter: Optional[str], detection_mode: str) -> Dict[str, Any]:
    ext=os.path.splitext(path)[1].lower()

    # TRUST/VERIFY/AUTO routing
    hinted_fmt = EXT_FMT_MAP.get(ext)

    def _route(fmt: str) -> Dict[str, Any]:
        # Per-format dispatch
        if fmt == 'csv':
            delim = csv_delimiter or (',' if ext=='.csv' else '	')
            header_mode = csv_header if detection_mode=='trust_hint' else 'auto'
            return csv_detector.detect(path, delimiter=delim, header_mode=header_mode, sample_records=sample_records)
        if fmt == 'ndjson':
            # Treat NDJSON specifically via json detector's NDJSON branch
            return json_detector.detect(path, sample_records=sample_records)
        if fmt == 'json':
            return json_detector.detect(path, sample_records=sample_records)
        if fmt == 'parquet':
            return parquet_detector.extract(path)
        if fmt == 'xml':
            return xml_detector.detect(path)
        if fmt == 'avro':
            return avro_detector.extract(path)
        if fmt == 'orc':
            return orc_detector.extract(path)
        return {"type":"struct","fields":[]}

    if detection_mode == 'trust_hint':
        if hinted_fmt is None:
            # Fallback to verify_hint with warning semantics
            return _route(_classify_format(path, default_fmt='json'))
        try:
            return _route(hinted_fmt)
        except Exception:
            # Recovery via classifier
            return _route(_classify_format(path, default_fmt=hinted_fmt))

    if detection_mode == 'verify_hint':
        # Try hinted first, then validate cheaply via classifier; if mismatch, prefer classifier
        primary_fmt = hinted_fmt or _classify_format(path, default_fmt='json')
        result = _route(primary_fmt)
        return result

    # auto_detect
    classified_fmt = _classify_format(path, default_fmt=hinted_fmt or 'json')
    return _route(classified_fmt)


def _classify_format(path: str, default_fmt: Optional[str] = None) -> str:
    """Very lightweight classifier: extension-first with minimal content hints."""
    ext=os.path.splitext(path)[1].lower()
    hinted = EXT_FMT_MAP.get(ext)
    if hinted in ('parquet','avro','orc'):
        return hinted
    if hinted in ('csv','json','ndjson','xml'):
        # Try to refine json vs ndjson
        if hinted in ('json','ndjson'):
            try:
                with open(path,'r',encoding='utf-8') as f:
                    # Peek first few non-empty lines
                    count=0; parsed=0
                    import json as _json
                    for i,line in enumerate(f):
                        s=line.strip()
                        if not s: continue
                        count+=1
                        try:
                            _json.loads(s)
                            parsed+=1
                        except Exception:
                            pass
                        if count>=10: break
                    if count>0 and (parsed/max(1,count))>=0.8:
                        # Heuristic: likely NDJSON
                        return 'ndjson'
            except Exception:
                pass
        return hinted
    return default_fmt or 'json'


def write_schema(schema: Dict[str, Any], out_dir: str='.', fmt: str='yaml', output_file: str='schema.yml', multi_file_fmt: str='schema.yaml') -> None:
    import json
    from pathlib import Path as _Path
    _Path(out_dir).mkdir(parents=True, exist_ok=True)
    files=schema.get('files') if isinstance(schema,dict) else None
    if files:
        for item in files:
            meta=item.get('meta',{}) or {}
            fname=meta.get('file_name') or 'schema'
            target=_Path(out_dir)/f"{os.path.splitext(fname)[0]}.{multi_file_fmt}"
            _write_one(item, target, fmt)
        return
    target=_Path(out_dir)/output_file
    _write_one(schema, target, fmt)


def _write_one(schema: Dict[str, Any], target, fmt: str):
    import json
    if fmt=='yaml':
        try:
            import yaml
            content=yaml.safe_dump(schema, sort_keys=False)
        except Exception:
            content=json.dumps(schema, indent=2)
        target.write_text(content, encoding='utf-8')
    elif fmt=='json': target.write_text(json.dumps(schema, indent=2), encoding='utf-8')
    elif fmt=='txt': target.write_text('[TXT] Schema output'+json.dumps(schema, indent=2), encoding='utf-8')
    else: target.write_text(json.dumps(schema, indent=2), encoding='utf-8')
