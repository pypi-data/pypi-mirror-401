def recommend_actions(root_cause: str) -> list[str]:
    if root_cause == "Connection pool exhausted":
        return [
            "Increase database connection pool size",
            "Restart affected service",
            "Monitor latency for 15 minutes",
        ]

    if root_cause == "Database unavailable":
        return [
            "Check database health",
            "Failover to replica",
            "Notify database team",
        ]

    if root_cause == "Invalid or expired credentials":
        return [
            "Rotate credentials",
            "Redeploy service",
            "Verify access permissions",
        ]

    return ["Escalate to on-call engineer"]
