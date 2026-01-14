from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Set

class GuardrailViolation(RuntimeError):
    pass

@dataclass(frozen=True)
class Guardrails:
    max_steps: int = 10
    max_tool_calls: int = 20
    max_cost_usd: float = 1.00
    deterministic: bool = True
    allowed_tools: Optional[Set[str]] = None

    def validate_tool_allowed(self, tool_name: str) -> None:
        if self.allowed_tools is not None and tool_name not in self.allowed_tools:
            raise GuardrailViolation(f"Tool '{tool_name}' is not allowlisted.")

    def validate_limits(self, steps: int, tool_calls: int, cost_usd: float) -> None:
        if steps > self.max_steps:
            raise GuardrailViolation(f"Max steps exceeded: {steps} > {self.max_steps}")
        if tool_calls > self.max_tool_calls:
            raise GuardrailViolation(f"Max tool calls exceeded: {tool_calls} > {self.max_tool_calls}")
        if cost_usd > self.max_cost_usd:
            raise GuardrailViolation(f"Max cost exceeded: {cost_usd:.4f} > {self.max_cost_usd:.4f}")
