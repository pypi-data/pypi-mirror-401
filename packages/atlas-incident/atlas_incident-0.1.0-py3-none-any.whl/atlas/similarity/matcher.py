from typing import Optional, Tuple
from atlas.schemas.incident import Incident


def _score(a: Incident, b: Incident) -> int:
    score = 0
    if a.category == b.category:
        score += 3
    if a.service == b.service:
        score += 2

    a_words = set(a.summary.lower().split())
    b_words = set(b.summary.lower().split())
    score += len(a_words & b_words)

    return score


def find_similar(
    current: Incident,
    history: list[Incident],
) -> Tuple[Optional[Incident], int]:
    best_match = None
    best_score = 0

    for past in history:
        s = _score(current, past)
        if s > best_score:
            best_score = s
            best_match = past

    return best_match, best_score
