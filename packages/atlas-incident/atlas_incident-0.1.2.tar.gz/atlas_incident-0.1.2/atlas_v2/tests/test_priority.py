from atlas.schemas.incident import Incident
from atlas_v2.priority.scorer import PriorityScorer

def test_priority_p0_db_prod():
    inc = Incident(
        service="payments",
        environment="prod",
        severity="CRITICAL",
        category="db",
        summary="db timeout"
    )
    decision = PriorityScorer().score(inc)
    assert decision.priority == "P0"
    assert decision.score >= 90
