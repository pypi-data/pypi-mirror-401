from atlas.recommendations.actions import recommend_actions


def test_db_pool_actions():
    actions = recommend_actions("Connection pool exhausted")
    assert "Restart affected service" in actions
