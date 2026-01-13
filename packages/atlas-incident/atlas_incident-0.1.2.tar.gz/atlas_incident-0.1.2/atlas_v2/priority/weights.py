SEVERITY_WEIGHTS = {
    "CRITICAL": 40,
    "HIGH": 30,
    "MEDIUM": 20,
    "LOW": 10,
}

ENV_WEIGHTS = {
    "prod": 30,
    "staging": 10,
    "dev": 0,
}

CATEGORY_WEIGHTS = {
    "db": 20,
    "auth": 25,
    "cache": 10,
    None: 0,
}

PRIORITY_BUCKETS = [
    (90, "P0"),
    (60, "P1"),
    (30, "P2"),
    (0,  "P3"),
]
