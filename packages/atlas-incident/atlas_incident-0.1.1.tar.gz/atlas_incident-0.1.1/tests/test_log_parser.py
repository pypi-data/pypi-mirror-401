from atlas.parsing.log_parser import parse_logs


def test_basic_log_parsing():
    logs = "ERROR database timeout\nINFO service started"
    parsed = parse_logs(logs)

    assert len(parsed) == 2
    assert parsed[0].level == "ERROR"
    assert parsed[1].level == "INFO"
