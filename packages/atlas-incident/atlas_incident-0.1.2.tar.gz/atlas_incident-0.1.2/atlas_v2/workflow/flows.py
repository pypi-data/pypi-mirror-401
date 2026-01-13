from atlas_v2.workflow.definitions import Workflow, WorkflowStep

DB_OUTAGE_WORKFLOW = Workflow(
    workflow_id="db_outage",
    steps=[
        WorkflowStep("notify_oncall"),
        WorkflowStep("wait_5_min"),
        WorkflowStep("check_errors"),
        WorkflowStep("restart_service"),
        WorkflowStep("escalate"),
    ]
)
