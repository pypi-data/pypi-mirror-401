from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class ParsedLog:
    level: Optional[str]
    message: str
    raw: str


def parse_logs(raw_logs: str) -> List[ParsedLog]:
    results: List[ParsedLog] = []

    for line in raw_logs.splitlines():
        line = line.strip()
        if not line:
            continue

        level = None
        if line.startswith("ERROR"):
            level = "ERROR"
        elif line.startswith("WARN"):
            level = "WARN"
        elif line.startswith("INFO"):
            level = "INFO"

        message = line.split(" ", 1)[1] if level else line
        results.append(ParsedLog(level=level, message=message, raw=line))

    return results
