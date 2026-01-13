from atlas_v2.state.store import WorkflowState
from atlas_v2.audit.trail import AuditTrail
from .definitions import Workflow


class WorkflowEngine:
    def __init__(self, audit: AuditTrail):
        self.audit = audit

    def step(self, workflow: Workflow, state: WorkflowState) -> WorkflowState:
        if state.completed:
            return state

        if state.current_step >= len(workflow.steps):
            state.completed = True
            self.audit.record(f"{workflow.workflow_id}: completed")
            return state

        step = workflow.steps[state.current_step]
        self.audit.record(
            f"{workflow.workflow_id}: executing step {step.name}"
        )

        # deterministic: step always "succeeds" for now
        state.current_step += 1
        return state
