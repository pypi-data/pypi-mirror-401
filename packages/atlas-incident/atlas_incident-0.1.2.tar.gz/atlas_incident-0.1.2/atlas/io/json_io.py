import json
from typing import Any


def to_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True)
