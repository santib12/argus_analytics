"""
Argus Phase 2 — Database connection helpers
==========================================

File: src/database/connection.py
Depends on: src/config/settings.py  (DATABASE_URL from .env)

GOAL
----
Provide a small, reusable way to connect to PostgreSQL from Python scripts,
ingestion code, and (later) FastAPI.
"""

from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.config.logging import get_logger
from src.config.settings import get_settings

logger = get_logger(__name__)

# Module-level engine cache (one Engine per process).
_ENGINE: Engine | None = None


def get_engine() -> Engine:
    """Return a shared SQLAlchemy Engine (created once)."""
    global _ENGINE

    if _ENGINE is None:
        settings = get_settings()
        _ENGINE = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            future=True,
        )

    return _ENGINE


def get_connection():
    """Open a SQLAlchemy connection from the shared engine."""
    engine = get_engine()
    return engine.connect()


def check_connection() -> bool:
    """Return True if SELECT 1 succeeds against DATABASE_URL."""
    try:
        with get_connection() as conn:
            result = conn.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception:
        logger.exception("Database connection check failed")
        raise
