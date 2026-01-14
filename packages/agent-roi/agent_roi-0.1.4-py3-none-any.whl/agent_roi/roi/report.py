# src/agent_roi/roi/report.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


def _fmt_usd(x: float, decimals: int = 2) -> str:
    return f"${x:,.{decimals}f}"


def _safe_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default


def _risk_rank(risk: str) -> int:
    """
    Lower is better (preferred earlier in sorting).

    We explicitly prefer low-risk over high-risk on ties.
    Unknown/unset risks should be LAST in a tie-break.
    """
    r = (risk or "").strip().lower()
    if r in ("low",):
        return 0
    if r in ("med", "medium"):
        return 1
    if r in ("high",):
        return 2
    return 3  # unknown last


def _summarize_risks(recs: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {"low": 0, "med": 0, "high": 0, "unknown": 0}
    for r in recs:
        risk = (r.get("risk") or "").strip().lower()
        if risk in ("low", "med", "high"):
            counts[risk] += 1
        elif risk == "medium":
            counts["med"] += 1
        else:
            counts["unknown"] += 1
    return counts


def _compute_payback_display(run_cost_usd: float, monthly_savings_usd: float) -> Tuple[Optional[float], str]:
    """
    Returns (payback_days, human_display_string).
    """
    if monthly_savings_usd <= 0:
        return None, "N/A"

    daily = monthly_savings_usd / 30.0
    if daily <= 0:
        return None, "N/A"

    days = (run_cost_usd / daily) if run_cost_usd > 0 else 0.0

    # Human-friendly display
    if run_cost_usd <= 0:
        return 0.0, "< 1 minute"

    if days < (1.0 / 24.0):  # < 1 hour
        minutes = max(1.0, days * 24.0 * 60.0)
        return days, f"~{minutes:,.0f} minutes"
    if days < 1.0:
        hours = days * 24.0
        return days, f"~{hours:,.1f} hours"
    if days < 30.0:
        return days, f"~{days:,.1f} days"
    months = days / 30.0
    return days, f"~{months:,.1f} months"


def _compute_roi_multiple(run_cost_usd: float, monthly_savings_usd: float) -> Tuple[Optional[float], str]:
    """
    Returns (roi_multiple, human_display_string).
    """
    if run_cost_usd <= 0:
        return None, "N/A"
    multiple = monthly_savings_usd / run_cost_usd
    if multiple >= 1000:
        return multiple, f"{multiple:,.0f}×"
    if multiple >= 100:
        return multiple, f"{multiple:,.1f}×"
    return multiple, f"{multiple:,.2f}×"


def _infer_monthly_savings(summary: Any, recs: List[Dict[str, Any]]) -> float:
    """
    Prefer summary-provided total savings; else sum recommendation savings.
    """
    if isinstance(summary, dict):
        val = summary.get("est_total_monthly_savings_usd", None)
        if val is not None:
            return _safe_float(val, 0.0)
    return sum(_safe_float(r.get("est_monthly_savings_usd", 0.0), 0.0) for r in recs)


def _infer_num_scanned(summary: Any) -> int:
    if isinstance(summary, dict):
        return int(_safe_float(summary.get("num_resources_scanned", 0), 0.0))
    return 0


def _infer_num_recs(summary: Any, recs: List[Dict[str, Any]]) -> int:
    if isinstance(summary, dict):
        v = summary.get("num_recommendations", None)
        if v is not None:
            return int(_safe_float(v, float(len(recs))))
    return int(len(recs))


def _infer_run_cost_usd(sentinel_result: Any, agent_output: Any) -> float:
    # 1) True run cost tracked by SentinelRunner
    ctx_snapshot = getattr(sentinel_result, "ctx_snapshot", {}) or {}
    run_cost = _safe_float(ctx_snapshot.get("state", {}).get("cost_usd", 0.0), 0.0)
    if run_cost > 0:
        return run_cost

    # 2) Some tests / minimal outputs put cost in agent_output.meta.cost_usd
    if isinstance(agent_output, dict):
        meta = agent_output.get("meta", {}) if isinstance(agent_output.get("meta", {}), dict) else {}
        run_cost = _safe_float(meta.get("cost_usd", 0.0), 0.0)
        if run_cost > 0:
            return run_cost

    return 0.0


@dataclass(frozen=True)
class ROIReport:
    title: str
    generated_at_utc: str
    correlation_id: str
    run_id: str

    decision_outcome: str
    decision_confidence: float

    estimated_monthly_savings_usd: float
    estimated_run_cost_usd: float
    roi_multiple_monthly: Optional[float]
    roi_multiple_display: str
    payback_days: Optional[float]
    payback_display: str

    num_resources_scanned: int
    num_recommendations: int
    risk_counts: Dict[str, int]

    top_recommendations: List[Dict[str, Any]]
    notes: List[str]

    # --- dict-like convenience (keeps tests backward-compatible) ---
    def __getitem__(self, key: str) -> Any:
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "generated_at_utc": self.generated_at_utc,
            "correlation_id": self.correlation_id,
            "run_id": self.run_id,
            "decision_outcome": self.decision_outcome,
            "decision_confidence": self.decision_confidence,
            "estimated_monthly_savings_usd": self.estimated_monthly_savings_usd,
            "estimated_run_cost_usd": self.estimated_run_cost_usd,
            "roi_multiple_monthly": self.roi_multiple_monthly,
            "roi_multiple_display": self.roi_multiple_display,
            "payback_days": self.payback_days,
            "payback_display": self.payback_display,
            "num_resources_scanned": self.num_resources_scanned,
            "num_recommendations": self.num_recommendations,
            "risk_counts": dict(self.risk_counts),
            "top_recommendations": list(self.top_recommendations),
            "notes": list(self.notes),
        }

    def to_markdown(self) -> str:
        low = self.risk_counts.get("low", 0)
        med = self.risk_counts.get("med", 0)
        high = self.risk_counts.get("high", 0)
        unknown = self.risk_counts.get("unknown", 0)

        lines: List[str] = []
        lines.append(f"# {self.title}")
        lines.append("")
        lines.append("> **Executive Summary:** This run generated actionable cloud cost-optimization recommendations with")
        lines.append(f"> projected savings of **{_fmt_usd(self.estimated_monthly_savings_usd)} / month**.")
        lines.append("")

        lines.append("## Overview")
        lines.append(f"- Generated (UTC): **{self.generated_at_utc}**")
        lines.append(f"- Correlation ID: `{self.correlation_id}`")
        lines.append(f"- Run ID: `{self.run_id}`")
        lines.append("")

        lines.append("## Governance Decision")
        lines.append(f"- Outcome: **{self.decision_outcome}**")
        lines.append(f"- Confidence score: **{self.decision_confidence:.3f}**")
        lines.append("")

        lines.append("## ROI Summary")
        lines.append(f"- Estimated monthly savings: **{_fmt_usd(self.estimated_monthly_savings_usd)}**")
        lines.append(f"- Estimated run cost: **{_fmt_usd(self.estimated_run_cost_usd, decimals=4)}**")
        lines.append(f"- ROI multiple (monthly savings / run cost): **{self.roi_multiple_display}**")
        lines.append(f"- Payback period: **{self.payback_display}**")
        lines.append("")

        lines.append("## Scope and Risk Breakdown")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|---|---:|")
        lines.append(f"| Resources scanned | {self.num_resources_scanned:,} |")
        lines.append(f"| Recommendations generated | {self.num_recommendations:,} |")
        lines.append(f"| Low risk | {low:,} |")
        lines.append(f"| Medium risk | {med:,} |")
        lines.append(f"| High risk | {high:,} |")
        if unknown:
            lines.append(f"| Unknown risk | {unknown:,} |")
        lines.append("")

        lines.append("## Recommended Next Actions")
        if high > 0:
            lines.append(f"- **Owner approval required:** {high} high-risk recommendation(s).")
        if med > 0:
            lines.append(f"- **Validate before scheduling changes:** {med} medium-risk recommendation(s).")
        if low > 0:
            lines.append(f"- **Candidate for fast-track remediation:** {low} low-risk recommendation(s) (after standard checks).")
        if self.num_recommendations == 0:
            lines.append("- No actions recommended in this run.")
        lines.append("")

        lines.append("## Top Recommendations (by estimated monthly savings)")
        lines.append("")
        if not self.top_recommendations:
            lines.append("_No recommendations generated._")
            lines.append("")
        else:
            lines.append("| Rank | Resource | Type | Action | Risk | Est. savings / month | Rationale |")
            lines.append("|---:|---|---|---|---|---:|---|")
            for i, r in enumerate(self.top_recommendations, start=1):
                rid = str(r.get("resource_id", r.get("id", "")))
                rtype = str(r.get("resource_type", ""))
                action = str(r.get("action", ""))
                risk = str(r.get("risk", ""))
                savings = _safe_float(r.get("est_monthly_savings_usd", 0.0))
                rationale = str(r.get("rationale", "")).replace("\n", " ").strip()
                lines.append(
                    f"| {i} | `{rid}` | {rtype} | {action} | {risk} | {_fmt_usd(savings)} | {rationale} |"
                )
            lines.append("")

        if self.notes:
            lines.append("## Notes")
            for n in self.notes:
                lines.append(f"- {n}")
            lines.append("")

        return "\n".join(lines)


def build_finops_roi_report(
    sentinel_result: Any,
    agent_output: Dict[str, Any] | None = None,
    *,
    title: str | None = None,
    period: str | None = None,
    top_n: int = 5,
) -> ROIReport:
    """
    Build a FinOps ROI report.

    Backwards compatible:
      - Allows positional `sentinel_result`
      - Accepts legacy `period=` kwarg (used to decorate the title)
      - If `agent_output` is omitted, attempts to use `sentinel_result.output`
    """
    generated_at_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    if agent_output is None:
        agent_output = getattr(sentinel_result, "output", None) or getattr(sentinel_result, "agent_output", None)
        if agent_output is None:
            raise TypeError(
                "build_finops_roi_report() missing agent_output. "
                "Pass agent_output=... or provide sentinel_result.output."
            )
    if not isinstance(agent_output, dict):
        raise TypeError("build_finops_roi_report() expected agent_output as a dict-like object.")

    if title is None:
        base = "Agent Sentinel ROI Report (FinOps)"
        title = f"{base} ({period})" if period else base

    summary = agent_output.get("summary", {}) if isinstance(agent_output.get("summary", {}), dict) else {}
    recs = agent_output.get("recommendations", [])
    if not isinstance(recs, list):
        recs = []

    monthly_savings = _infer_monthly_savings(summary, recs)
    num_scanned = _infer_num_scanned(summary)
    num_recs = _infer_num_recs(summary, recs)

    run_cost = _infer_run_cost_usd(sentinel_result, agent_output)

    # Decision fields
    outcome_obj = getattr(sentinel_result, "outcome", "")
    decision_outcome = getattr(outcome_obj, "value", str(outcome_obj))
    decision_conf = float(getattr(sentinel_result, "confidence", 0.0))

    # Sort: savings desc, then lower risk first (low before high), then stable by id/resource
    recs_sorted = sorted(
        recs,
        key=lambda r: (
            -_safe_float(r.get("est_monthly_savings_usd", 0.0), 0.0),
            _risk_rank(str(r.get("risk", ""))),
            str(r.get("resource_id", r.get("id", ""))),
        ),
    )
    top_recs = recs_sorted[: max(0, int(top_n))]

    roi_multiple, roi_display = _compute_roi_multiple(run_cost, monthly_savings)
    payback_days, payback_display = _compute_payback_display(run_cost, monthly_savings)
    risk_counts = _summarize_risks(recs)

    notes: List[str] = [
        "Savings are estimates; validate with real utilization + pricing data before acting.",
        "High-risk actions should require explicit owner approval and a rollback plan.",
        "Audit events are recorded in an append-only log to support traceability and governance review.",
    ]

    return ROIReport(
        title=title,
        generated_at_utc=generated_at_utc,
        correlation_id=str(getattr(sentinel_result, "correlation_id", "")),
        run_id=str(getattr(sentinel_result, "run_id", "")),
        decision_outcome=decision_outcome,
        decision_confidence=decision_conf,
        estimated_monthly_savings_usd=float(monthly_savings),
        estimated_run_cost_usd=float(run_cost),
        roi_multiple_monthly=roi_multiple,
        roi_multiple_display=roi_display,
        payback_days=payback_days,
        payback_display=payback_display,
        num_resources_scanned=int(num_scanned),
        num_recommendations=int(num_recs),
        risk_counts=risk_counts,
        top_recommendations=top_recs,
        notes=notes,
    )
