from atlas.schemas.incident import Incident
from atlas_v2.rules.engine import RuleEngine
from atlas_v2.rules.rules import Rule

def test_rule_fires():
    rule = Rule(
        "R1",
        "test rule",
        lambda inc, pr: pr == "P0"
    )
    engine = RuleEngine([rule])

    inc = Incident("svc", "prod", "CRITICAL", "db", "x")
    fired = engine.evaluate(inc, "P0")
    assert len(fired) == 1
