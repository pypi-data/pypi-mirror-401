from atlas.parsing.log_parser import parse_logs
from atlas.normalization.normalizer import normalize_incident
from atlas.classification.classifier import classify_incident
from atlas.rca.engine import determine_root_cause
from atlas.recommendations.actions import recommend_actions
from atlas.history.store import save_incident


def run_pipeline(
    raw_logs: str,
    service: str,
    environment: str,
) -> dict:
    logs = parse_logs(raw_logs)
    incident = normalize_incident(service, environment, logs)
    incident = classify_incident(incident)
    root_cause = determine_root_cause(incident)
    actions = recommend_actions(root_cause)

    confidence = 0.5
    if incident.category != "UNKNOWN":
        confidence += 0.2
    if root_cause != "Unknown root cause":
        confidence += 0.2
    if actions:
        confidence += 0.1

    result = {
        "service": incident.service,
        "environment": incident.environment,
        "severity": incident.severity,
        "category": incident.category,
        "root_cause": root_cause,
        "actions": actions,
        "confidence": round(confidence, 2),
    }

    save_incident(result)
    return result
