
"""Detect schema from a Pandas DataFrame."""
from typing import Dict, Any

def detect_schema_from_df(df) -> Dict[str, Any]:
    try:
        import pandas as pd
        import pandas.api.types as pat
    except Exception:
        # Lazy import failure fallback
        raise RuntimeError('Pandas is required for pandas_df schema detection')

    fields = []
    for name in df.columns:
        series = df[name]
        t = 'string'
        if pat.is_bool_dtype(series):
            t = 'boolean'
        elif pat.is_integer_dtype(series):
            t = 'integer'
        elif pat.is_float_dtype(series):
            t = 'double'
        elif pat.is_datetime64_any_dtype(series):
            # Prefer timestamp; date-only detection could be added if all times are 00:00:00
            t = 'timestamp'
        elif pat.is_object_dtype(series):
            t = 'string'
        nullable = bool(series.isna().any())
        fields.append({"name": str(name), "type": t, "nullable": nullable, "metadata": {}})

    return {"type": "struct", "fields": fields, "meta": {"source": "pandas_df"}}
