from atlas.schemas.incident import Incident
from atlas.parsing.log_parser import ParsedLog


def normalize_incident(
    service: str,
    environment: str,
    logs: list[ParsedLog],
) -> Incident:
    severity = "LOW"
    summary = "Unknown issue"

    for log in logs:
        if log.level == "ERROR":
            severity = "HIGH"
            summary = log.message
            break

    return Incident(
        service=service,
        environment=environment,
        severity=severity,
        category=None,
        summary=summary,
    )
