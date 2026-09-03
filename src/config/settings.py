"""Application settings loaded from environment variables.

Secrets belong in `.env` (never committed). Use `.env.example` as the template.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _load_env() -> None:
    """Load `.env` from the project root if present."""
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(dotenv_path=env_path, override=False)


@dataclass(frozen=True)
class Settings:
    """Typed runtime configuration for Argus."""

    database_url: str
    usaspending_base_url: str
    sam_api_key: str
    openai_api_key: str
    log_level: str

    @property
    def has_sam_api_key(self) -> bool:
        return bool(self.sam_api_key.strip())

    @property
    def has_openai_api_key(self) -> bool:
        return bool(self.openai_api_key.strip())


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings loaded from the environment."""
    _load_env()
    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:password@localhost:5432/argus",
        ),
        usaspending_base_url=os.getenv(
            "USASPENDING_BASE_URL",
            "https://api.usaspending.gov",
        ).rstrip("/"),
        sam_api_key=os.getenv("SAM_API_KEY", ""),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )


# Convenience singleton for `from src.config.settings import settings`
settings = get_settings()
