from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional
import hashlib, json, time, uuid

def _stable_json(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    correlation_id: str
    run_id: str
    ts_epoch_ms: int
    event_type: str
    payload: Dict[str, Any]
    prev_hash: Optional[str] = None
    hash: Optional[str] = None

    @staticmethod
    def create(correlation_id: str, run_id: str, event_type: str, payload: Dict[str, Any],
               prev_hash: Optional[str], hash_chain: bool) -> "AuditEvent":
        base = {
            "event_id": str(uuid.uuid4()),
            "correlation_id": correlation_id,
            "run_id": run_id,
            "ts_epoch_ms": int(time.time() * 1000),
            "event_type": event_type,
            "payload": payload,
            "prev_hash": prev_hash,
        }
        event_hash = None
        if hash_chain:
            h = hashlib.sha256()
            h.update(_stable_json(base).encode("utf-8"))
            event_hash = h.hexdigest()

        return AuditEvent(
            event_id=base["event_id"],
            correlation_id=correlation_id,
            run_id=run_id,
            ts_epoch_ms=base["ts_epoch_ms"],
            event_type=event_type,
            payload=payload,
            prev_hash=prev_hash,
            hash=event_hash,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "correlation_id": self.correlation_id,
            "run_id": self.run_id,
            "ts_epoch_ms": self.ts_epoch_ms,
            "event_type": self.event_type,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "hash": self.hash,
        }
