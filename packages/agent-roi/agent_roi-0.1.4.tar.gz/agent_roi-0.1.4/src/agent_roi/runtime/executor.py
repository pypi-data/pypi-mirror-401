from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Union, cast

from .context import SentinelContext
from ..control.guardrails import Guardrails
from ..control.decision import DecisionPolicy, ConfidenceInputs, DecisionOutcome
from ..audit.event import AuditEvent
from ..audit.store import JsonlAuditStore, AuditStore


@dataclass
class SentinelResult:
    outcome: DecisionOutcome
    confidence: float
    output: Any
    correlation_id: str
    run_id: str
    ctx_snapshot: Dict[str, Any]


def _safe_repr(value: Any, *, max_len: int = 2000) -> str:
    try:
        s = repr(value)
        return s if len(s) <= max_len else s[: max_len - 3] + "..."
    except Exception:
        return "<unreprable>"


class SentinelRunner:
    def __init__(
        self,
        *,
        name: str = "sentinel_run",
        guardrails: Optional[Guardrails] = None,
        decision_policy: Optional[DecisionPolicy] = None,
        audit_store: Optional[AuditStore] = None,
        audit_hash_chain: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.guardrails = guardrails or Guardrails()
        self.decision_policy = decision_policy or DecisionPolicy()
        self.audit_store = audit_store or JsonlAuditStore(hash_chain=audit_hash_chain)
        self.audit_hash_chain = audit_hash_chain
        self.metadata = metadata or {}

    def _log(self, ctx: SentinelContext, event_type: str, payload: Dict[str, Any]) -> None:
        prev = self.audit_store.last_hash(ctx.correlation_id)
        event = AuditEvent.create(
            correlation_id=ctx.correlation_id,
            run_id=ctx.run_id,
            event_type=event_type,
            payload=payload,
            prev_hash=prev,
            hash_chain=self.audit_hash_chain,
        )
        self.audit_store.append(event)

    def _normalize_agent_return(
        self,
        agent_return: Any,
    ) -> Tuple[Any, Optional[ConfidenceInputs]]:
        """
        Supports:
          - output
          - (output, ConfidenceInputs)
        """
        if (
            isinstance(agent_return, tuple)
            and len(agent_return) == 2
            and isinstance(agent_return[1], ConfidenceInputs)
        ):
            output, ci = cast(Tuple[Any, ConfidenceInputs], agent_return)
            return output, ci

        return agent_return, None

    def run(
        self,
        agent_fn: Callable[[SentinelContext, Any], Any],
        input_data: Any,
        *,
        confidence_inputs: Optional[ConfidenceInputs] = None,
    ) -> SentinelResult:
        started = time.time()

        ctx = SentinelContext(
            metadata={"name": self.name, **(self.metadata or {})},
            guardrails=self.guardrails,
        )

        self._log(
            ctx,
            "run_start",
            {
                "input_type": str(type(input_data)),
                "ctx": ctx.snapshot(),
            },
        )

        try:
            ctx.bump_step()

            # Backstop validation (ctx bump_step already validates, but this is harmless)
            self.guardrails.validate_limits(ctx.state.steps, ctx.state.tool_calls, ctx.state.cost_usd)

            agent_return = agent_fn(ctx, input_data)
            output, ci_from_agent = self._normalize_agent_return(agent_return)

            self._log(
                ctx,
                "agent_output",
                {
                    "output_type": str(type(output)),
                    "output_preview": _safe_repr(output),
                },
            )

            # Select confidence inputs in priority order:
            #   1) explicit runner.run(confidence_inputs=...)
            #   2) agent returned (output, ConfidenceInputs)
            #   3) neutral default so decision isn't always abstain
            ci = confidence_inputs or ci_from_agent or ConfidenceInputs(llm_self_score=0.5)

            conf = self.decision_policy.score(ci)
            outcome = self.decision_policy.decide(ci)

            elapsed_ms = int((time.time() - started) * 1000)

            self._log(
                ctx,
                "decision",
                {
                    "confidence": conf,
                    "outcome": outcome.value,
                    "inputs": ci.__dict__,
                },
            )
            self._log(
                ctx,
                "run_end",
                {
                    "status": "ok",
                    "elapsed_ms": elapsed_ms,
                    "ctx": ctx.snapshot(),
                },
            )

            return SentinelResult(
                outcome=outcome,
                confidence=conf,
                output=output,
                correlation_id=ctx.correlation_id,
                run_id=ctx.run_id,
                ctx_snapshot=ctx.snapshot(),
            )

        except Exception as e:
            elapsed_ms = int((time.time() - started) * 1000)
            self._log(
                ctx,
                "run_error",
                {
                    "error_type": type(e).__name__,
                    "message": str(e),
                    "elapsed_ms": elapsed_ms,
                    "ctx": ctx.snapshot(),
                },
            )
            self._log(ctx, "run_end", {"status": "error", "elapsed_ms": elapsed_ms, "ctx": ctx.snapshot()})
            raise
