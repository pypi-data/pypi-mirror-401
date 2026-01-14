from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import csv

from agent_roi.policies.loader import Policy


@dataclass(frozen=True)
class Finding:
    finding_type: str
    severity: str
    evidence: Dict[str, Any]
    recommendation: Dict[str, Any]
    record: Dict[str, Any]


class ProcurementLeakageAnalyzer:
    """
    Fortune-5 style spend leakage demo:
      - duplicate invoices
      - price variance vs baseline
      - unapproved vendor flags
    """

    def __init__(self, policy: Policy, business_context: Dict[str, Any]) -> None:
        self.policy = policy
        self.ctx = business_context
        self.thresholds = policy.data.get("thresholds", {})
        self.multipliers = policy.data.get("scoring", {}).get("savings_multipliers", {})

    def analyze(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        invoices = payload.get("invoices", [])
        approved_vendors = set(payload.get("approved_vendors", []))
        baseline_prices = payload.get("baseline_unit_prices", {})  # sku -> price

        findings: List[Finding] = []

        # Detect duplicates by (vendor, invoice_id, amount)
        seen: set[Tuple[str, str, float]] = set()
        dup_th = self.thresholds.get("duplicate_invoice", {})
        dup_amt_gt = float(dup_th.get("amount_usd_gt", 1000.0))

        for inv in invoices:
            vendor = inv.get("vendor", "unknown")
            invoice_id = inv.get("invoice_id", "")
            amount = float(inv.get("amount_usd", 0.0))
            key = (vendor, invoice_id, amount)

            if key in seen and amount > dup_amt_gt:
                action = "duplicate_invoice"
                savings = round(amount * float(self.multipliers.get(action, 1.0)), 2)
                findings.append(Finding(
                    finding_type="duplicate_payment_risk",
                    severity="high",
                    evidence={"vendor": vendor, "invoice_id": invoice_id, "amount_usd": amount},
                    recommendation={
                        "action": action,
                        "est_monthly_savings_usd": savings,
                        "risk": "med",
                        "rationale": "Duplicate invoice signature detected. Recommend payment hold + review.",
                    },
                    record=inv
                ))
            else:
                seen.add(key)

            # Unapproved vendor
            if self.thresholds.get("unapproved_vendor", {}).get("always_flag", True):
                if vendor not in approved_vendors and vendor != "unknown":
                    action = "unapproved_vendor"
                    savings = round(amount * float(self.multipliers.get(action, 0.40)), 2)
                    findings.append(Finding(
                        finding_type="vendor_compliance_risk",
                        severity="medium",
                        evidence={"vendor": vendor},
                        recommendation={
                            "action": action,
                            "est_monthly_savings_usd": savings,
                            "risk": "med",
                            "rationale": "Vendor not in approved list. Recommend onboarding check + contract validation.",
                        },
                        record=inv
                    ))

            # Price variance (sku)
            sku = inv.get("sku")
            qty = float(inv.get("qty", 0))
            if sku in baseline_prices and qty > 0:
                baseline = float(baseline_prices[sku])
                unit = float(inv.get("unit_price_usd", 0))
                pct = ((unit - baseline) / baseline) * 100.0 if baseline > 0 else 0.0
                pv_th = self.thresholds.get("price_variance", {})
                if pct > float(pv_th.get("pct_gt", 15.0)):
                    action = "price_variance"
                    # estimate recoverable as portion of delta
                    delta_total = (unit - baseline) * qty
                    savings = round(delta_total * float(self.multipliers.get(action, 0.60)), 2)
                    findings.append(Finding(
                        finding_type="price_variance",
                        severity="high",
                        evidence={"sku": sku, "baseline_unit_price": baseline, "unit_price": unit, "pct_over": round(pct, 1)},
                        recommendation={
                            "action": action,
                            "est_monthly_savings_usd": savings,
                            "risk": "high",
                            "rationale": f"Unit price {pct:.1f}% above baseline. Recommend contract check + vendor dispute.",
                        },
                        record=inv
                    ))

        # Recommendations
        recs: List[Dict[str, Any]] = []
        for f in findings:
            inv = f.record
            rec = dict(f.recommendation)
            rec.update({
                "record_id": inv.get("record_id"),
                "vendor": inv.get("vendor"),
                "invoice_id": inv.get("invoice_id"),
                "business_unit": inv.get("business_unit", "unknown"),
            })
            recs.append(rec)

        total = round(sum(float(r.get("est_monthly_savings_usd", 0.0)) for r in recs), 2)

        return {
            "summary": {
                "program": self.ctx.get("program", "Procurement Spend Leakage"),
                "reporting_period": self.ctx.get("reporting_period"),
                "num_records_scanned": len(invoices),
                "num_findings": len(findings),
                "num_recommendations": len(recs),
                "est_total_monthly_savings_usd": total,
            },
            "recommendations": recs,
            "assumptions": self.ctx.get("assumptions", []),
        }

    def export_recommendations_csv(self, agent_output: Dict[str, Any], out_path: str) -> None:
        recs = agent_output.get("recommendations", []) or []
        fieldnames = [
            "record_id", "vendor", "invoice_id", "business_unit",
            "action", "risk", "est_monthly_savings_usd", "rationale"
        ]
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in recs:
                w.writerow({k: r.get(k, "") for k in fieldnames})
