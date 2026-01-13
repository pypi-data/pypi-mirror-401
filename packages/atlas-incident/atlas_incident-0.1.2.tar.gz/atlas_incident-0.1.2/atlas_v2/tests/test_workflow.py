from atlas_v2.workflow.engine import WorkflowEngine
from atlas_v2.state.store import WorkflowState
from atlas_v2.audit.trail import AuditTrail
from atlas_v2.workflow.definitions import Workflow, WorkflowStep


def test_workflow_progression():
    wf = Workflow(
        "test",
        [WorkflowStep("a"), WorkflowStep("b")]
    )
    audit = AuditTrail()
    engine = WorkflowEngine(audit)
    state = WorkflowState("test")

    state = engine.step(wf, state)
    assert state.current_step == 1

    state = engine.step(wf, state)
    assert state.current_step == 2

    state = engine.step(wf, state)
    assert state.completed is True
