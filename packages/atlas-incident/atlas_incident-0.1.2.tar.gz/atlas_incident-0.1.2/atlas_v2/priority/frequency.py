import json
from pathlib import Path

class FrequencyTracker:
    def __init__(self, window_sec=300):
        # project root → incident_history.jsonl
        self.path = Path(__file__).resolve().parents[2] / "incident_history.jsonl"
        self.window = window_sec

    def count(self, key: str) -> int:
        if not self.path.exists():
            return 0

        cnt = 0
        with self.path.open() as f:
            for line in f:
                r = json.loads(line)
                k = f"{r['service']}:{r.get('category')}:{r['environment']}"
                if k == key:
                    cnt += 1
        return cnt
