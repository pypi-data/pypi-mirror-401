from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DecisionOutcome(str, Enum):
    ACCEPT = "accept"
    ABSTAIN = "abstain"
    HUMAN_REVIEW = "human_review"
    RETRY = "retry"


@dataclass(frozen=True)
class ConfidenceInputs:
    prob: Optional[float] = None
    margin: Optional[float] = None
    z_score: Optional[float] = None
    entropy: Optional[float] = None
    llm_self_score: Optional[float] = None


@dataclass(frozen=True)
class DecisionPolicy:
    min_confidence: float = 0.75
    abstain_action: DecisionOutcome = DecisionOutcome.HUMAN_REVIEW

    # weights
    w_prob: float = 0.55
    w_margin: float = 0.20
    w_z: float = 0.15
    w_entropy: float = 0.10  # treated as penalty
    w_llm: float = 0.10

    def score(self, x: ConfidenceInputs) -> float:
        def clamp01(v: float) -> float:
            return max(0.0, min(1.0, v))

        score = 0.0
        weight_sum = 0.0

        if x.prob is not None:
            score += self.w_prob * clamp01(float(x.prob))
            weight_sum += abs(self.w_prob)

        if x.margin is not None:
            score += self.w_margin * clamp01(float(x.margin))
            weight_sum += abs(self.w_margin)

        if x.z_score is not None:
            # logistic transform maps real-valued z into (0,1)
            z = float(x.z_score)
            z01 = 1.0 / (1.0 + math.exp(-z))
            score += self.w_z * clamp01(z01)
            weight_sum += abs(self.w_z)

        if x.entropy is not None:
            # Normalize entropy to [0,1] assuming ~0..2.5 typical scale; cap safely
            e = float(x.entropy)
            e01 = clamp01(e / 2.5)
            # penalty: higher entropy reduces confidence
            score -= abs(self.w_entropy) * e01
            weight_sum += abs(self.w_entropy)

        if x.llm_self_score is not None:
            score += self.w_llm * clamp01(float(x.llm_self_score))
            weight_sum += abs(self.w_llm)

        if weight_sum == 0.0:
            return 0.0

        return clamp01(score / weight_sum)

    def decide(self, x: ConfidenceInputs) -> DecisionOutcome:
        return DecisionOutcome.ACCEPT if self.score(x) >= self.min_confidence else self.abstain_action
