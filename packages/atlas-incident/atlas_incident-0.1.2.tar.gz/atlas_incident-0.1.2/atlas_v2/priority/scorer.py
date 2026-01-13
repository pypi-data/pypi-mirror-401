from typing import List
from atlas.schemas.incident import Incident
from .weights import (
    SEVERITY_WEIGHTS,
    ENV_WEIGHTS,
    CATEGORY_WEIGHTS,
    PRIORITY_BUCKETS,
)
from atlas_v2.schemas.decision import PriorityDecision
from atlas_v2.priority.frequency import FrequencyTracker


class PriorityScorer:
    tracker = FrequencyTracker()

    def score(self, incident: Incident) -> PriorityDecision:
        score = 0
        reasons: List[str] = []

        sev = SEVERITY_WEIGHTS.get(incident.severity.upper(), 0)
        score += sev
        reasons.append(f"severity={incident.severity} (+{sev})")

        env = ENV_WEIGHTS.get(incident.environment.lower(), 0)
        score += env
        reasons.append(f"environment={incident.environment} (+{env})")

        cat = CATEGORY_WEIGHTS.get(incident.category, 0)
        score += cat
        reasons.append(f"category={incident.category} (+{cat})")

        # ✅ frequency logic (INSIDE method)
        key = f"{incident.service}:{incident.category}:{incident.environment}"
        freq = self.tracker.count(key)

        if freq >= 20:
            score += 30
            reasons.append(f"high frequency ({freq}/5min) (+30)")
        elif freq >= 5:
            score += 10
            reasons.append(f"medium frequency ({freq}/5min) (+10)")

        priority = self._bucket(score)
        return PriorityDecision(priority=priority, score=score, reasons=reasons)

    @staticmethod
    def _bucket(score: int) -> str:
        for threshold, label in PRIORITY_BUCKETS:
            if score >= threshold:
                return label
        return "P3"
