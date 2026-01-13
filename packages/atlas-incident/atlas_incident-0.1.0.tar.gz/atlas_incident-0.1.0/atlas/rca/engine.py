from atlas.schemas.incident import Incident


def determine_root_cause(incident: Incident) -> str:
    summary = incident.summary.lower()

    if incident.category == "DATABASE":
        if "timeout" in summary:
            return "Connection pool exhausted"
        if "refused" in summary:
            return "Database unavailable"

    if incident.category == "NETWORK":
        return "Network resolution failure"

    if incident.category == "AUTH":
        return "Invalid or expired credentials"

    return "Unknown root cause"
