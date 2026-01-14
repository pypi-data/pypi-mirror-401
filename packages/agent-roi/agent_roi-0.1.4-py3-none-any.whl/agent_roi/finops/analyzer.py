from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List
import csv

from agent_roi.policies.loader import Policy


@dataclass(frozen=True)
class Finding:
    finding_type: str
    severity: str
    evidence: Dict[str, Any]
    recommendation: Dict[str, Any]
    resource: Dict[str, Any]


class FinOpsAnalyzer:
    """
    Enterprise-style analyzer:
      - Findings are separated from recommendations
      - Governance (thresholds, multipliers, routing) comes from policy YAML
      - Output is deterministic and audit-friendly
    """

    def __init__(self, policy: Policy, business_context: Dict[str, Any]) -> None:
        self.policy = policy
        self.ctx = business_context

        self.multipliers = policy.data.get("scoring", {}).get("savings_multipliers", {})
        self.thresholds = policy.data.get("thresholds", {})
        self.routing = policy.data.get("approval_routing", {})

    def approval_status(self, resource: Dict[str, Any], risk: str) -> str:
        env = (resource.get("environment") or "").lower()
        risk_l = (risk or "").lower()
        prod_risks = set((self.routing.get("production_requires_approval_for_risk") or []))
        if env == "production" and risk_l in prod_risks:
            return "owner_approval_required"
        return "auto_approve_candidate"

    def analyze(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        resources = payload.get("resources", [])
        findings: List[Finding] = []

        for r in resources:
            rtype = r.get("type")
            cost = float(r.get("monthly_cost_usd", 0.0))
            util = float(r.get("utilization_pct", 0.0))
            idle_days = int(r.get("days_idle", 0))

            # EC2: underutilized
            if rtype == "ec2_instance":
                th = self.thresholds.get("underutilized_compute", {})
                if util < float(th.get("utilization_pct_lt", 10.0)) and cost > float(th.get("monthly_cost_usd_gt", 200.0)):
                    action = "rightsizing_recommendation"
                    savings = round(cost * float(self.multipliers.get(action, 0.35)), 2)
                    risk = "med" if (r.get("environment", "").lower() == "production") else "low"
                    findings.append(Finding(
                        finding_type="underutilized_compute",
                        severity="high",
                        evidence={"utilization_pct": util, "monthly_cost_usd": cost},
                        recommendation={"action": action, "est_monthly_savings_usd": savings, "risk": risk,
                                        "rationale": f"Low utilization ({util:.1f}%). Recommend downsizing."},
                        resource=r
                    ))
                    continue

                th = self.thresholds.get("idle_compute", {})
                if idle_days >= int(th.get("idle_days_gte", 14)) and cost > float(th.get("monthly_cost_usd_gt", 50.0)):
                    action = "scheduled_stop"
                    savings = round(cost * float(self.multipliers.get(action, 0.65)), 2)
                    findings.append(Finding(
                        finding_type="idle_compute",
                        severity="medium",
                        evidence={"days_idle": idle_days, "monthly_cost_usd": cost},
                        recommendation={"action": action, "est_monthly_savings_usd": savings, "risk": "low",
                                        "rationale": f"Idle for {idle_days} days. Recommend schedule/stop."},
                        resource=r
                    ))
                    continue

            # EBS: orphaned
            if rtype == "ebs_volume":
                attached = bool(r.get("attached", True))
                if not attached and idle_days >= 7 and cost > 10:
                    action = "snapshot_then_delete"
                    savings = round(cost * float(self.multipliers.get(action, 0.90)), 2)
                    findings.append(Finding(
                        finding_type="orphaned_storage",
                        severity="medium",
                        evidence={"attached": False, "days_idle": idle_days},
                        recommendation={"action": action, "est_monthly_savings_usd": savings, "risk": "low",
                                        "rationale": "Unattached volume. Snapshot then delete."},
                        resource=r
                    ))
                    continue

            # RDS: underutilized db
            if rtype == "rds_instance":
                th = self.thresholds.get("underutilized_database", {})
                if util < float(th.get("utilization_pct_lt", 5.0)) and cost > float(th.get("monthly_cost_usd_gt", 300.0)):
                    action = "rightsizing_recommendation"
                    savings = round(cost * float(self.multipliers.get(action, 0.30)), 2)
                    findings.append(Finding(
                        finding_type="underutilized_database",
                        severity="high",
                        evidence={"utilization_pct": util, "monthly_cost_usd": cost},
                        recommendation={"action": action, "est_monthly_savings_usd": savings, "risk": "high",
                                        "rationale": f"Very low utilization ({util:.1f}%). Owner validation required."},
                        resource=r
                    ))
                    continue

            # S3: large bucket
            if rtype == "s3_bucket":
                th = self.thresholds.get("large_bucket", {})
                storage_gb = float(r.get("storage_gb", 0))
                if storage_gb > float(th.get("storage_gb_gt", 5000)):
                    action = "lifecycle_policy_to_infrequent_access"
                    savings = round(cost * float(self.multipliers.get(action, 0.20)), 2)
                    findings.append(Finding(
                        finding_type="storage_tiering_opportunity",
                        severity="low",
                        evidence={"storage_gb": storage_gb, "monthly_cost_usd": cost},
                        recommendation={"action": action, "est_monthly_savings_usd": savings, "risk": "low",
                                        "rationale": "Large bucket. Add lifecycle policy to cheaper storage class."},
                        resource=r
                    ))
                    continue

        # Build enterprise-ready recommendations
        recommendations: List[Dict[str, Any]] = []
        for f in findings:
            r = f.resource
            rec = dict(f.recommendation)
            rec.update({
                "resource_id": r.get("id"),
                "resource_type": r.get("type"),
                "environment": r.get("environment"),
                "owner": r.get("owner", "unknown"),
                "approval_status": self.approval_status(r, rec.get("risk", "")),
            })
            recommendations.append(rec)

        total_savings = round(sum(float(x.get("est_monthly_savings_usd", 0.0)) for x in recommendations), 2)

        return {
            "summary": {
                "program": self.ctx.get("program", "Cloud Cost Governance"),
                "reporting_period": self.ctx.get("reporting_period"),
                "num_resources_scanned": len(payload.get("resources", [])),
                "num_findings": len(findings),
                "num_recommendations": len(recommendations),
                "est_total_monthly_savings_usd": total_savings,
            },
            "recommendations": recommendations,
            "assumptions": self.ctx.get("assumptions", []),
        }

    def export_recommendations_csv(self, agent_output: Dict[str, Any], out_path: str) -> None:
        recs = agent_output.get("recommendations", []) or []
        fieldnames = [
            "resource_id", "resource_type", "environment", "owner",
            "action", "risk", "approval_status", "est_monthly_savings_usd", "rationale"
        ]
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in recs:
                w.writerow({k: r.get(k, "") for k in fieldnames})
