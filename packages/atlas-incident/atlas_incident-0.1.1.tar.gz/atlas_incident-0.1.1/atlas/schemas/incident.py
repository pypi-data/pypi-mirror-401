from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Incident:
    service: str
    environment: str
    severity: str
    category: Optional[str]
    summary: str
