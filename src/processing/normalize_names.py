"""
Phase 4 — Company / person name normalization
=============================================

Normalize legal entity names for matching and analytics without
changing raw source files under data/raw/.
"""

from __future__ import annotations

import re
from typing import Any

# Collapse runs of whitespace
_WHITESPACE_RE = re.compile(r"\s+")

# Common US legal suffixes → canonical token (applied after uppercasing)
_SUFFIX_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bL\.?\s*L\.?\s*C\.?\b"), "LLC"),
    (re.compile(r"\bL\.?\s*L\.?\s*P\.?\b"), "LLP"),
    (re.compile(r"\bINCORPORATED\b"), "INC"),
    (re.compile(r"\bINC\.?\b"), "INC"),
    (re.compile(r"\bCORPORATION\b"), "CORP"),
    (re.compile(r"\bCORP\.?\b"), "CORP"),
    (re.compile(r"\bCOMPANY\b"), "CO"),
    (re.compile(r"\bCO\.?\b"), "CO"),
    (re.compile(r"\bLIMITED\b"), "LTD"),
    (re.compile(r"\bLTD\.?\b"), "LTD"),
    (re.compile(r"\bP\.?\s*L\.?\s*C\.?\b"), "PLC"),
]


def normalize_company_name(value: Any) -> str | None:
    """
    Normalize a company / recipient name for matching.

    Rules (conservative):
      - None / blank → None (do not invent a name)
      - Uppercase
      - Collapse internal whitespace
      - Normalize common legal suffixes (L.L.C. → LLC, Inc. → INC, ...)
      - Remove leftover commas and periods
      - Strip outer whitespace

    Example:
      "ACME TECHNOLOGIES, L.L.C." → "ACME TECHNOLOGIES LLC"
    """
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    text = text.upper()
    text = _WHITESPACE_RE.sub(" ", text)

    for pattern, replacement in _SUFFIX_PATTERNS:
        text = pattern.sub(replacement, text)

    # Remove punctuation that usually does not carry identity signal
    text = text.replace(",", " ")
    text = text.replace(".", " ")
    text = _WHITESPACE_RE.sub(" ", text).strip()

    return text or None


def normalize_whitespace(value: Any) -> str | None:
    """Trim and collapse whitespace; blank → None."""
    if value is None:
        return None
    text = _WHITESPACE_RE.sub(" ", str(value).strip())
    return text or None
