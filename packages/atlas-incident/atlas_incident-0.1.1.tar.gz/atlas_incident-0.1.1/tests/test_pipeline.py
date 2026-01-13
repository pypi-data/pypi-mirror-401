from atlas.orchestrator.pipeline import run_pipeline


def test_full_pipeline():
    result = run_pipeline(
        raw_logs="ERROR db timeout",
        service="payments",
        environment="prod",
    )

    assert result["category"] == "DATABASE"
    assert result["confidence"] > 0.5
