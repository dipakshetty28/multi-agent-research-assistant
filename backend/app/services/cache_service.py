import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Optional


class FileCacheService:
    def __init__(self, cache_directory: str) -> None:
        self.base_path = Path(cache_directory)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _path_for_key(self, key: str) -> Path:
        return self.base_path / f"{key}.json"

    def build_key(self, payload: Dict[str, Any]) -> str:
        normalized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        path = self._path_for_key(key)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def set(self, key: str, value: Dict[str, Any]) -> None:
        path = self._path_for_key(key)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
