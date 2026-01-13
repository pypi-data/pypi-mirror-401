import json
from pathlib import Path
from typing import Iterator

HISTORY_FILE = Path("incident_history.jsonl")


def save_incident(record: dict) -> None:
    with HISTORY_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def load_history() -> Iterator[dict]:
    if not HISTORY_FILE.exists():
        return iter([])

    with HISTORY_FILE.open("r", encoding="utf-8") as f:
        return (json.loads(line) for line in f if line.strip())
