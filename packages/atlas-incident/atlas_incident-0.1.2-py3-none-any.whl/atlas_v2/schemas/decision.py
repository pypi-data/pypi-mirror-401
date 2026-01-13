from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PriorityDecision:
    priority: str          # P0, P1, P2, P3
    score: int
    reasons: List[str]


@dataclass(frozen=True)
class RuleDecision:
    rule_id: str
    description: str
