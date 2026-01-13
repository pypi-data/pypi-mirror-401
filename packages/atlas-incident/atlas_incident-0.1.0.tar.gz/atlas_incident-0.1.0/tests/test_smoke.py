from atlas.config.settings import load_settings
from atlas.schemas.incident import Incident


def test_settings_load() -> None:
    settings = load_settings()
    assert settings.app_name == "ATLAS"


def test_incident_schema() -> None:
    incident = Incident(
        service="payments-api",
        environment="production",
        severity="HIGH",
        category=None,
        summary="Database timeout",
    )
    assert incident.service == "payments-api"
