from typing import List
from atlas.schemas.incident import Incident
from atlas_v2.schemas.decision import RuleDecision
from .rules import Rule


class RuleEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def evaluate(self, incident: Incident, priority: str) -> List[RuleDecision]:
        fired: List[RuleDecision] = []
        for rule in self.rules:
            if rule.predicate(incident, priority):
                fired.append(
                    RuleDecision(
                        rule_id=rule.rule_id,
                        description=rule.description
                    )
                )
        return fired
