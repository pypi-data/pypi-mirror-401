from atlas.schemas.incident import Incident
from atlas.rca.engine import determine_root_cause


def test_db_timeout_root_cause():
    inc = Incident("svc", "prod", "HIGH", "DATABASE", "DB timeout")
    assert determine_root_cause(inc) == "Connection pool exhausted"
