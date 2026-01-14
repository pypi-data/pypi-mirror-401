from __future__ import annotations

from dataclasses import dataclass, field
import time
import uuid
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    # Avoid runtime circular imports while still giving type-checkers the right info.
    from agent_roi.control.guardrails import Guardrails

T = TypeVar("T")


@dataclass
class RunState:
    steps: int = 0
    tool_calls: int = 0
    cost_usd: float = 0.0


@dataclass
class SentinelContext:
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at_epoch_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    metadata: Dict[str, Any] = field(default_factory=dict)
    state: RunState = field(default_factory=RunState)

    # NEW: Attach guardrails so the context can enforce policy at runtime.
    guardrails: Optional["Guardrails"] = None

    def bump_step(self) -> None:
        self.state.steps += 1
        # Optional: enforce limits on every step bump if guardrails are provided.
        if self.guardrails is not None:
            self.guardrails.validate_limits(
                self.state.steps, self.state.tool_calls, self.state.cost_usd
            )

    def bump_tool_call(self) -> None:
        self.state.tool_calls += 1
        # Optional: enforce limits on every tool call bump if guardrails are provided.
        if self.guardrails is not None:
            self.guardrails.validate_limits(
                self.state.steps, self.state.tool_calls, self.state.cost_usd
            )

    def add_cost(self, amount_usd: float) -> None:
        self.state.cost_usd += float(amount_usd)
        # Optional: enforce limits on every cost update if guardrails are provided.
        if self.guardrails is not None:
            self.guardrails.validate_limits(
                self.state.steps, self.state.tool_calls, self.state.cost_usd
            )

    def call_tool(
        self,
        tool_name: str,
        fn: Callable[..., T],
        *args: Any,
        cost_usd: float = 0.0,
        **kwargs: Any,
    ) -> T:
        """
        Preferred way to invoke tools inside an agent.

        Enforces:
          - tool allowlist (if configured)
          - tool call counting
          - optional cost accounting
          - runtime limits (steps/tool_calls/cost) continuously
        """
        if self.guardrails is not None:
            self.guardrails.validate_tool_allowed(tool_name)

        self.bump_tool_call()

        if cost_usd:
            self.add_cost(cost_usd)

        # Execute tool
        return fn(*args, **kwargs)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "correlation_id": self.correlation_id,
            "run_id": self.run_id,
            "started_at_epoch_ms": self.started_at_epoch_ms,
            "metadata": self.metadata,
            "state": {
                "steps": self.state.steps,
                "tool_calls": self.state.tool_calls,
                "cost_usd": self.state.cost_usd,
            },
        }
