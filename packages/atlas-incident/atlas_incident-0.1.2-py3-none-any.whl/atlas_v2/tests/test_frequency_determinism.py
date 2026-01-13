from atlas.schemas.incident import Incident
from atlas_v2.priority.scorer import PriorityScorer

def test_deterministic_scoring():
    inc = Incident("svc", "prod", "HIGH", "db", "x")
    s1 = PriorityScorer().score(inc)
    s2 = PriorityScorer().score(inc)
    assert s1.score == s2.score
    assert s1.priority == s2.priority
