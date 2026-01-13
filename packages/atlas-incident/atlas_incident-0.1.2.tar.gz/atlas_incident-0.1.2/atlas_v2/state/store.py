from dataclasses import dataclass


@dataclass
class WorkflowState:
    workflow_id: str
    current_step: int = 0
    retries: int = 0
    completed: bool = False
