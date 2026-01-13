from atlas.schemas.incident import Incident


def classify_incident(incident: Incident) -> Incident:
    summary = incident.summary.lower()

    if "timeout" in summary or "connection" in summary:
        category = "DATABASE"
    elif "401" in summary or "403" in summary:
        category = "AUTH"
    elif "dns" in summary or "resolve" in summary:
        category = "NETWORK"
    else:
        category = "UNKNOWN"

    return Incident(
        service=incident.service,
        environment=incident.environment,
        severity=incident.severity,
        category=category,
        summary=incident.summary,
    )
