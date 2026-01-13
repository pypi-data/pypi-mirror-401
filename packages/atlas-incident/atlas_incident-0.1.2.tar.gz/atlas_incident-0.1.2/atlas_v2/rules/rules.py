from typing import Callable
from atlas.schemas.incident import Incident


class Rule:
    def __init__(self, rule_id: str, description: str,
                 predicate: Callable[[Incident, str], bool]):
        self.rule_id = rule_id
        self.description = description
        self.predicate = predicate
