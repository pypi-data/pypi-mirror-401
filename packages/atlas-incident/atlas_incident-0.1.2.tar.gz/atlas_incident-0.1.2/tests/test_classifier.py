from atlas.schemas.incident import Incident
from atlas.classification.classifier import classify_incident


def test_db_classification():
    incident = Incident("svc", "prod", "HIGH", None, "DB timeout occurred")
    classified = classify_incident(incident)

    assert classified.category == "DATABASE"
