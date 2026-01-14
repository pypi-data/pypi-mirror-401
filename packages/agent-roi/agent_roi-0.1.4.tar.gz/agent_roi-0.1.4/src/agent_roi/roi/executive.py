from __future__ import annotations

from typing import Any, Dict, List
from datetime import datetime, timezone


def build_executive_brief(
    *,
    title: str,
    business_context: Dict[str, Any],
    sentinel_result: Any,
    agent_output: Dict[str, Any],
    top_n: int = 5,
) -> str:
    summary = agent_output.get("summary", {}) if isinstance(agent_output, dict) else {}
    recs = agent_output.get("recommendations", []) if isinstance(agent_output, dict) else []
    recs = recs if isinstance(recs, list) else []

    # Sort by savings desc
    recs_sorted = sorted(recs, key=lambda r: float(r.get("est_monthly_savings_usd", 0.0)), reverse=True)
    top = recs_sorted[:top_n]

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    outcome_obj = getattr(sentinel_result, "outcome", "")
    outcome = getattr(outcome_obj, "value", str(outcome_obj))
    conf = float(getattr(sentinel_result, "confidence", 0.0))

    monthly = float(summary.get("est_total_monthly_savings_usd", 0.0))

    lines: List[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**Generated (UTC):** {generated}")
    lines.append(f"**Program:** {business_context.get('program', '')}")
    lines.append(f"**Reporting Period:** {business_context.get('reporting_period', '')}")
    lines.append("")
    lines.append("## Key Takeaways")
    lines.append(f"- Estimated savings identified: **${monthly:,.2f}/month**")
    lines.append(f"- Governance decision: **{outcome}** (confidence **{conf:.3f}**)")
    lines.append(f"- Recommendations produced: **{int(summary.get('num_recommendations', len(recs)))}**")
    lines.append("")
    lines.append("## Top Opportunities")
    if not top:
        lines.append("_No recommendations generated._")
    else:
        for r in top:
            rid = r.get("resource_id") or r.get("record_id") or "item"
            action = r.get("action", "")
            risk = r.get("risk", "")
            savings = float(r.get("est_monthly_savings_usd", 0.0))
            lines.append(f"- **{action}** on `{rid}` — **${savings:,.2f}/mo** (risk: `{risk}`)")
    lines.append("")
    lines.append("## Controls Applied")
    lines.append("- Execution guardrails (steps/tool calls/cost ceilings)")
    lines.append("- Confidence-based routing (auto vs human review)")
    lines.append("- Append-only audit logging (traceable run metadata)")
    lines.append("")
    lines.append("## Assumptions")
    for a in business_context.get("assumptions", []):
        lines.append(f"- {a}")
    lines.append("")
    return "\n".join(lines)
