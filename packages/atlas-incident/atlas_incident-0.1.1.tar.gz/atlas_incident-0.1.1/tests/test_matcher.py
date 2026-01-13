from atlas.schemas.incident import Incident
from atlas.similarity.matcher import find_similar


def test_similarity_match():
    current = Incident("svc", "prod", "HIGH", "DATABASE", "db timeout")
    past = Incident("svc", "prod", "HIGH", "DATABASE", "db connection timeout")

    match, score = find_similar(current, [past])
    assert match == past
    assert score > 0
