
"""Normalized schema model & Spark StructType conversion (MVP skeleton)."""
from typing import Dict, Any, List

class NormalizedSchema:
    def __init__(self, name: str = None, location: str = None, fmt: str = None):
        self.name = name
        self.location = location
        self.format = fmt
        self.fields: List[Dict[str, Any]] = []
        self.partitions: List[Dict[str, Any]] = []
        self.version = None
        self.properties: Dict[str, Any] = {}

    def to_spark_json(self) -> Dict[str, Any]:
        return {
            "type": "struct",
            "fields": self.fields,
        }
