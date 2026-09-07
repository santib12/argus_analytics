"""
Phase 4 — Award field normalization (dates, money, codes)
=======================================================

Type-safe parsers for award/transaction fields. Returns None for missing
or invalid values — never invents data.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any


def normalize_date(value: Any) -> date | None:
    """Parse a date-like value to datetime.date, or None."""
    if value is None or value == "":
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    text = str(value).strip()[:10]
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def normalize_money(value: Any) -> Decimal | None:
    """Parse a money-like value to Decimal, or None. Does not treat 0 as missing."""
    if value is None or value == "":
        return None
    try:
        text = str(value).strip().replace(",", "").replace("$", "")
        if text == "":
            return None
        return Decimal(text)
    except (InvalidOperation, ValueError):
        return None


def normalize_code(value: Any, *, max_len: int | None = None) -> str | None:
    """Uppercase/strip a short code (NAICS, PSC, agency). Blank → None."""
    if value is None:
        return None
    text = str(value).strip().upper()
    if not text:
        return None
    if max_len is not None:
        text = text[:max_len]
    return text
