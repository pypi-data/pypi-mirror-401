from __future__ import annotations

import argparse
import os
from typing import Optional

from agent_roi import SentinelRunner, Guardrails, DecisionPolicy, ConfidenceInputs
from agent_roi.policies import load_policy
from agent_roi.finops import FinOpsAnalyzer
from agent_roi.roi.report import build_finops_roi_report
from agent_roi.roi.executive import build_executive_brief
from agent_roi.runtime.artifacts import create_artifact_dir, write_manifest


BUSINESS_CONTEXT = {
    "program": "Cloud Cost Governance",
    "business_unit": "Enterprise Infrastructure",
    "reporting_period": "2026-01",
    "currency": "USD",
    "assumptions": [
        "Savings estimates are conservative",
        "No production changes executed automatically",
        "High-risk actions require owner approval",
        "All decisions are audited",
    ],
}


def _confidence_for_mode(mode: str) -> ConfidenceInputs:
    mode = (mode or "review").strip().lower()
    if mode == "accept":
        # Designed to exceed typical min_confidence >= 0.75
        return ConfidenceInputs(prob=0.99, margin=0.80, z_score=3.0, entropy=0.05, llm_self_score=0.95)
    if mode == "review":
        # Designed to fall below min_confidence ~0.75 and route to HUMAN_REVIEW
        return ConfidenceInputs(prob=0.80, margin=0.18, z_score=1.2, entropy=0.60, llm_self_score=0.70)
    raise ValueError("Invalid --mode. Use: accept|review")


def _build_demo_payload(policy_path: Optional[str]) -> dict:
    return {
        "estimated_cost_usd": 0.02,
        "policy_path": policy_path,
        "resources": [
            {
                "id": "ec2-prod-payments-01",
                "type": "ec2_instance",
                "owner": "payments",
                "environment": "production",
                "monthly_cost_usd": 520,
                "utilization_pct": 6.2,
            },
            {
                "id": "rds-prod-orders",
                "type": "rds_instance",
                "owner": "orders",
                "environment": "production",
                "monthly_cost_usd": 860,
                "utilization_pct": 2.0,
            },
            {
                "id": "s3-central-logs",
                "type": "s3_bucket",
                "owner": "security",
                "environment": "shared",
                "monthly_cost_usd": 310,
                "storage_gb": 9200,
            },
        ],
    }


def _make_finops_agent(confidence: ConfidenceInputs):
    def finops_agent(ctx, payload):
        if not hasattr(ctx, "call_tool"):
            raise RuntimeError(
                "SentinelContext.call_tool() not found. "
                "Update src/agent_roi/runtime/context.py and wire guardrails into executor."
            )

        estimated_cost = float(payload.get("estimated_cost_usd", 0.02))

        # Tool 1: policy load (audited + allowlisted)
        policy = ctx.call_tool(
            "policy_load",
            load_policy,
            "finops_policy.yaml",
            override_path=payload.get("policy_path"),
            cost_usd=0.0,
        )

        analyzer = FinOpsAnalyzer(policy=policy, business_context=BUSINESS_CONTEXT)

        # Tool 2: analysis (audited + allowlisted + costed)
        output = ctx.call_tool(
            "finops_analyze",
            analyzer.analyze,
            payload,
            cost_usd=estimated_cost,
        )

        return output, confidence

    return finops_agent


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agent-roi",
        description="Agent-ROI CLI demo (golden path): guardrails + audit + decision routing + ROI artifacts.",
    )
    parser.add_argument(
        "--policy",
        dest="policy_path",
        default=None,
        help="Path to an override policy YAML file (enterprise-managed).",
    )
    parser.add_argument(
        "--outdir",
        dest="outdir",
        default=None,
        help="Output directory for artifacts. Default: creates a timestamped folder under artifacts/.",
    )
    parser.add_argument(
        "--mode",
        dest="mode",
        default="review",
        choices=["accept", "review"],
        help="Demo mode to intentionally drive decision routing. accept => high confidence; review => human_review.",
    )

    args = parser.parse_args(argv)

    if args.policy_path is not None and not os.path.exists(args.policy_path):
        parser.error(f"--policy file not found: {args.policy_path}")

    # Load base policy (bundled) but allow override path
    base_policy = load_policy("finops_policy.yaml", override_path=args.policy_path)

    # Make Guardrails config robust to YAML list types
    guardrails_cfg = dict(base_policy.data.get("guardrails", {}))
    allowed = guardrails_cfg.get("allowed_tools")
    if isinstance(allowed, list):
        guardrails_cfg["allowed_tools"] = set(allowed)

    runner = SentinelRunner(
        name="cli_finops_demo",
        guardrails=Guardrails(**guardrails_cfg),
        decision_policy=DecisionPolicy(**base_policy.data.get("decision_policy", {})),
        metadata=BUSINESS_CONTEXT,
    )

    payload = _build_demo_payload(args.policy_path)
    confidence = _confidence_for_mode(args.mode)
    agent_fn = _make_finops_agent(confidence)

    result = runner.run(agent_fn, payload)

    # Artifacts directory
    artifacts = create_artifact_dir("finops") if args.outdir is None else args.outdir
    os.makedirs(artifacts, exist_ok=True)

    report = build_finops_roi_report(
        sentinel_result=result,
        agent_output=result.output,
        title="Cloud Cost Governance ROI Report",
    )

    brief = build_executive_brief(
        title="Cloud Cost Governance — Executive Brief",
        business_context=BUSINESS_CONTEXT,
        sentinel_result=result,
        agent_output=result.output,
    )

    analyzer = FinOpsAnalyzer(policy=base_policy, business_context=BUSINESS_CONTEXT)
    analyzer.export_recommendations_csv(result.output, f"{artifacts}/recommendations.csv")

    with open(f"{artifacts}/roi_report.md", "w", encoding="utf-8") as f:
        f.write(report.to_markdown())
    with open(f"{artifacts}/executive_brief.md", "w", encoding="utf-8") as f:
        f.write(brief)

    write_manifest(
        artifact_dir=artifacts,
        demo_name="finops",
        business_context=BUSINESS_CONTEXT,
        decision_outcome=result.outcome.value,
        confidence=result.confidence,
    )

    # Run summary (what users want to see)
    print("\nRun summary")
    print(f"  mode:        {args.mode}")
    print(f"  outcome:     {result.outcome.value}")
    print(f"  confidence:  {result.confidence:.3f}")
    print(f"  steps:       {result.ctx_snapshot['state']['steps']}")
    print(f"  tool_calls:  {result.ctx_snapshot['state']['tool_calls']}")
    print(f"  cost_usd:    {result.ctx_snapshot['state']['cost_usd']:.4f}")
    print(f"\nArtifacts written to: {artifacts}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
