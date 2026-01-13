from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class WorkflowStep:
    name: str


@dataclass(frozen=True)
class Workflow:
    workflow_id: str
    steps: List[WorkflowStep]
