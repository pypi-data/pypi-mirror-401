from atlas.normalization.normalizer import normalize_incident
from atlas.parsing.log_parser import ParsedLog


def test_error_sets_high_severity():
    logs = [ParsedLog(level="ERROR", message="DB timeout", raw="")]
    incident = normalize_incident("payments", "prod", logs)

    assert incident.severity == "HIGH"
