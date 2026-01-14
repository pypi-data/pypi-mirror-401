from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict, Optional, Protocol

from .event import AuditEvent, _stable_json


class AuditStore(Protocol):
    def append(self, event: AuditEvent) -> None: ...
    def last_hash(self, correlation_id: str) -> Optional[str]: ...


@dataclass
class JsonlAuditStore:
    """
    Simple JSONL-backed audit store.

    Notes:
      - `last_hash()` is cached per correlation_id to avoid O(n^2) behavior when logging
        many events into a large JSONL file.
      - Cache is built on first access and updated on append().
    """
    path: str = "sentinel_audit.jsonl"
    hash_chain: bool = True

    _last_hash_cache: Dict[str, str] = field(default_factory=dict, init=False, repr=False)
    _cache_built: bool = field(default=False, init=False, repr=False)

    def _ensure_dir(self) -> None:
        directory = os.path.dirname(self.path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def _build_cache(self) -> None:
        if self._cache_built:
            return
        if not os.path.exists(self.path):
            self._cache_built = True
            return

        last: Dict[str, str] = {}
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                cid = obj.get("correlation_id")
                h = obj.get("hash")
                if cid and h:
                    last[str(cid)] = str(h)

        self._last_hash_cache = last
        self._cache_built = True

    def append(self, event: AuditEvent) -> None:
        self._ensure_dir()
        payload = event.to_dict()

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(_stable_json(payload))
            f.write("\n")

        # Keep cache hot
        cid = payload.get("correlation_id")
        h = payload.get("hash")
        if cid and h:
            self._last_hash_cache[str(cid)] = str(h)
            self._cache_built = True

    def last_hash(self, correlation_id: str) -> Optional[str]:
        self._build_cache()
        return self._last_hash_cache.get(str(correlation_id))
