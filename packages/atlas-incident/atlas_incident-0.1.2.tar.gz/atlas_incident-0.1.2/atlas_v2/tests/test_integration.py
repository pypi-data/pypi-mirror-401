from atlas.schemas.incident import Incident
from atlas_v2.integration.controller import AtlasV2Controller
from atlas_v2.rules.definitions import RULES
from atlas_v2.workflow.flows import DB_OUTAGE_WORKFLOW


def test_full_v2_flow():
    controller = AtlasV2Controller(
        rules=RULES,
        workflows={"R-DB-P0": DB_OUTAGE_WORKFLOW}
    )

    inc = Incident(
        service="payments",
        environment="prod",
        severity="CRITICAL",
        category="db",
        summary="db timeout"
    )

    result = controller.handle_incident(inc)

    assert result["priority"].priority == "P0"
    assert "notify_oncall" in result["actions"]
    assert "db_outage" in result["workflows"]
