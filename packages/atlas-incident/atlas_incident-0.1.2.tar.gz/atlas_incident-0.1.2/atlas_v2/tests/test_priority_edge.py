from atlas.schemas.incident import Incident
from atlas_v2.priority.scorer import PriorityScorer

def test_unknown_low_priority():
    inc = Incident(
        service="svc",
        environment="prod",
        severity="LOW",
        category="UNKNOWN",
        summary="x",
    )
    out = PriorityScorer().score(inc)
    assert out.priority in ("P2", "P3")
