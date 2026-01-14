from __future__ import annotations

from typing import Any, Dict, List


class PolicyValidationError(ValueError):
    pass


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _require_mapping(data: Dict[str, Any], key: str, errors: List[str]) -> Dict[str, Any]:
    val = data.get(key)
    if not isinstance(val, dict):
        errors.append(f"policy.{key} must be a mapping/object")
        return {}
    return val


def _require_number(
    obj: Dict[str, Any],
    path: str,
    key: str,
    errors: List[str],
    *,
    min_value: float | None = None,
    max_value: float | None = None,
    required: bool = False,
) -> None:
    if key not in obj:
        if required:
            errors.append(f"{path}.{key} is required")
        return

    v = obj.get(key)
    if not _is_number(v):
        errors.append(f"{path}.{key} must be a number")
        return

    fv = float(v)
    if min_value is not None and fv < min_value:
        errors.append(f"{path}.{key} must be >= {min_value}")
    if max_value is not None and fv > max_value:
        errors.append(f"{path}.{key} must be <= {max_value}")


def _require_int_like(
    obj: Dict[str, Any],
    path: str,
    key: str,
    errors: List[str],
    *,
    min_value: int | None = None,
    required: bool = False,
) -> None:
    if key not in obj:
        if required:
            errors.append(f"{path}.{key} is required")
        return

    v = obj.get(key)
    if not _is_number(v) or float(v) != int(float(v)):
        errors.append(f"{path}.{key} must be an integer")
        return

    iv = int(v)
    if min_value is not None and iv < min_value:
        errors.append(f"{path}.{key} must be >= {min_value}")


def _validate_allowed_tools(guardrails: Dict[str, Any], errors: List[str]) -> None:
    allowed = guardrails.get("allowed_tools")
    if allowed is None:
        # Optional: make this required if you want deny-by-default everywhere
        return

    if not isinstance(allowed, (list, set, tuple)):
        errors.append("policy.guardrails.allowed_tools must be a list (or set) of strings")
        return

    bad = [x for x in allowed if not isinstance(x, str) or not x.strip()]
    if bad:
        errors.append("policy.guardrails.allowed_tools must contain only non-empty strings")


def _validate_decision_weights(dp: Dict[str, Any], errors: List[str]) -> None:
    for k in ("w_prob", "w_margin", "w_z", "w_entropy", "w_llm"):
        if k in dp and not _is_number(dp[k]):
            errors.append(f"policy.decision_policy.{k} must be a number")

    # Entropy is treated as a penalty in score(); negative would invert meaning.
    if "w_entropy" in dp and _is_number(dp["w_entropy"]) and float(dp["w_entropy"]) < 0:
        errors.append("policy.decision_policy.w_entropy should be >= 0 (entropy is treated as a penalty)")


def validate_policy(data: Dict[str, Any]) -> None:
    errors: List[str] = []

    # --- guardrails ---
    guardrails = _require_mapping(data, "guardrails", errors)
    # IMPORTANT: validate even if dict is empty ({} should fail required fields)
    _require_int_like(guardrails, "policy.guardrails", "max_steps", errors, min_value=1, required=True)
    _require_int_like(guardrails, "policy.guardrails", "max_tool_calls", errors, min_value=0, required=True)
    _require_number(guardrails, "policy.guardrails", "max_cost_usd", errors, min_value=0.0, required=True)

    if "deterministic" in guardrails and not isinstance(guardrails["deterministic"], bool):
        errors.append("policy.guardrails.deterministic must be a boolean")

    _validate_allowed_tools(guardrails, errors)

    # --- decision policy ---
    dp = _require_mapping(data, "decision_policy", errors)
    # IMPORTANT: validate even if dict is empty
    _require_number(dp, "policy.decision_policy", "min_confidence", errors, min_value=0.0, max_value=1.0, required=True)

    if "abstain_action" in dp and not isinstance(dp["abstain_action"], str):
        errors.append("policy.decision_policy.abstain_action must be a string (e.g., 'human_review')")

    _validate_decision_weights(dp, errors)

    if errors:
        raise PolicyValidationError("Invalid policy:\n- " + "\n- ".join(errors))
