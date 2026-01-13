from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class Config:
    detection_mode: str = 'trust_hint'
    coverage_mode: str = 'max'
    sample_records: int = 500
    sample_bytes: str = '5MB'
    zip_max_size: str = '500MB'
    zip_max_members: int = 100
    sample_total_bytes_cap: str = '1GB'
    max_file_size: str = '50GB'
    retries: int = 3
    timeout_seconds: int = 180
    max_workers: Optional[int] = None
    log_json: bool = False
    verbosity: int = 0
    csv_header: str = 'auto'
    encoding: Optional[str] = None

    def merge_flags(self, flags: Dict[str, Any]):
        for k, v in flags.items():
            if hasattr(self, k) and v is not None:
                setattr(self, k, v)
        return self

    @staticmethod
    def from_yaml(path: Optional[str]):
        if not path:
            return Config()
        import yaml
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        cfg = Config()
        # Minimal mapping for MVP
        cfg.detection_mode = data.get('detection_mode', cfg.detection_mode)
        return cfg
