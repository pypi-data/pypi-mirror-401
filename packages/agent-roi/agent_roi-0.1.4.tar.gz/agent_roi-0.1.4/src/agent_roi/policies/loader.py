from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
from typing import Any, Dict, Optional

from .validate import validate_policy


@dataclass(frozen=True)
class Policy:
    name: str
    data: Dict[str, Any]


def _normalize_policy_in_place(data: Dict[str, Any]) -> None:
    """
    Normalize common policy fields after YAML load so downstream code gets
    consistent types (and users have fewer ways to accidentally misconfigure).
    """
    guardrails = data.get("guardrails")
    if isinstance(guardrails, dict):
        allowed = guardrails.get("allowed_tools")
        if isinstance(allowed, list):
            # YAML commonly loads sets as lists; normalize to set for runtime membership checks
            guardrails["allowed_tools"] = set(allowed)


def load_policy(package_yaml_name: str, *, override_path: Optional[str] = None) -> Policy:
    """
    Load a YAML policy either from:
      - a local override_path (recommended for enterprise usage), OR
      - bundled package policy file under agent_roi/policies/

    package_yaml_name examples:
      - "finops_policy.yaml"
      - "procurement_policy.yaml"
    """
    try:
        import yaml  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "PyYAML is required to load policy YAML. Install with: pip install PyYAML"
        ) from e

    if override_path:
        with open(override_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        _normalize_policy_in_place(data)
        validate_policy(data)  # ✅ validate override policies too
        return Policy(name=package_yaml_name, data=data)

    pkg = "agent_roi.policies"
    policy_path = files(pkg).joinpath(package_yaml_name)
    data = yaml.safe_load(policy_path.read_text(encoding="utf-8")) or {}
    _normalize_policy_in_place(data)
    validate_policy(data)  # ✅ validate bundled policy
    return Policy(name=package_yaml_name, data=data)
