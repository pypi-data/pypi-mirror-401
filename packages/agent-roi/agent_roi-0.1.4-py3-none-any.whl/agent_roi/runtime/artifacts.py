from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import json
import uuid
from typing import Dict, Any


def create_artifact_dir(demo_name: str, outdir: str | Path | None = None) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_id = uuid.uuid4().hex[:12]
    root = Path(outdir) if outdir else (Path("artifacts") / demo_name)
    path = root / f"{ts}_{run_id}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_manifest(
    artifact_dir: Path,
    *,
    demo_name: str,
    business_context: Dict[str, Any],
    decision_outcome: str,
    confidence: float,
) -> None:
    manifest = {
        "demo": demo_name,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "business_context": business_context,
        "decision_outcome": decision_outcome,
        "confidence": round(confidence, 4),
    }
    (artifact_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
