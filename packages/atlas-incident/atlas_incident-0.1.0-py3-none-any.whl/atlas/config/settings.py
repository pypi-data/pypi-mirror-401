from dataclasses import dataclass
from typing import Literal


Environment = Literal["production", "staging", "development"]


@dataclass(frozen=True)
class Settings:
    app_name: str
    environment: Environment
    debug: bool


def load_settings() -> Settings:
    # Deterministic defaults (no env magic yet)
    return Settings(
        app_name="ATLAS",
        environment="development",
        debug=True,
    )
