"""Detect schema from a Spark DataFrame, preserving logical types."""
from typing import Dict, Any

def _map_spark_type(t) -> (str, dict):
    """Map Spark SQL types to normalized type + metadata.
    Returns (type_str, metadata_dict)."""
    # Avoid hard imports to keep this module light; rely on class names
    cls_name = type(t).__name__
    md = {}

    if cls_name in ('StringType',):
        return 'string', md
    if cls_name in ('BooleanType',):
        return 'boolean', md
    if cls_name in ('ByteType','ShortType','IntegerType','LongType'):  # unify to integer
        return 'integer', md
    if cls_name in ('FloatType','DoubleType'):
        return 'double', md
    if cls_name == 'DecimalType':
        # Spark DecimalType has precision/scale attributes
        try:
            md = {"precision": getattr(t, 'precision'), "scale": getattr(t, 'scale'), "logical_type": "decimal"}
        except Exception:
            md = {"logical_type": "decimal"}
        return 'decimal', md
    if cls_name == 'DateType':
        return 'date', md
    if cls_name == 'TimestampType':
        return 'timestamp', md
    if cls_name == 'ArrayType':
        et, emd = _map_spark_type(getattr(t, 'elementType'))
        # element nullability available as containsNull
        return f"array<{et}>", {**md, **({'element_nullable': getattr(t, 'containsNull', True)}), **({'element_metadata': emd} if emd else {})}
    # StructType, MapType → treat as object for MVP
    return 'object', md


def detect_schema_from_df(df) -> Dict[str, Any]:
    schema = df.schema
    fields = []
    for f in schema.fields:
        t_str, md = _map_spark_type(f.dataType)
        nullable = bool(getattr(f, 'nullable', True))
        fields.append({"name": f.name, "type": t_str, "nullable": nullable, "metadata": md})
    return {"type": "struct", "fields": fields, "meta": {"source": "spark_df"}}
