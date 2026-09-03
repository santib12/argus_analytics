"""Shared logging helpers for Argus modules and scripts."""

from __future__ import annotations

import logging
import sys

from src.config.settings import get_settings

_CONFIGURED = False


def configure_logging(level: str | None = None) -> None:
    """Configure root logging once for the process."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    resolved_level = (level or get_settings().log_level).upper()
    logging.basicConfig(
        level=getattr(logging, resolved_level, logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )
    _CONFIGURED = True


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a named logger after ensuring logging is configured."""
    configure_logging()
    return logging.getLogger(name or "argus")
