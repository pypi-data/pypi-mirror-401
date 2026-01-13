from atlas_v2.rules.rules import Rule

RULES = [
    Rule(
        rule_id="R-DB-P0",
        description="DB incident with P0 priority",
        predicate=lambda inc, pr: inc.category == "db" and pr == "P0"
    ),
    Rule(
        rule_id="R-AUTH-PROD",
        description="Auth issue in production",
        predicate=lambda inc, pr: inc.category == "auth"
        and inc.environment == "prod"
    ),
]
