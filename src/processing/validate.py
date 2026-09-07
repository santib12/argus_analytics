"""
Phase 4 — Validation helpers
============================

Validate identifiers and collect reject reasons without mutating raw data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

# SAM / USAspending UEI: 12 alphanumeric characters (no O/I sometimes in docs;
# we accept A-Z0-9 after uppercasing for practicality).
_UEI_RE = re.compile(r"^[A-Z0-9]{12}$")


@dataclass
class ValidationResult:
    """Outcome of validating one field or row."""

    ok: bool
    value: Any = None
    reason: str | None = None


@dataclass
class RejectLog:
    """In-memory log of rejected rows/fields for DQ reporting."""

    entries: list[dict[str, Any]] = field(default_factory=list)

    def add(self, *, entity: str, key: str | None, reason: str, raw: Any = None) -> None:
        self.entries.append(
            {
                "entity": entity,
                "key": key,
                "reason": reason,
                "raw": None if raw is None else str(raw)[:200],
            }
        )

    def __len__(self) -> int:
        return len(self.entries)


def validate_uei(value: Any) -> ValidationResult:
    """
    Validate a Unique Entity Identifier.

    - None / blank → ok=False, reason missing (not invented)
    - Strip + uppercase
    - Must be exactly 12 A-Z / 0-9 characters
    """
    if value is None or str(value).strip() == "":
        return ValidationResult(ok=False, value=None, reason="uei_missing")

    cleaned = str(value).strip().upper()
    if not _UEI_RE.match(cleaned):
        return ValidationResult(ok=False, value=cleaned, reason="uei_invalid_format")

    return ValidationResult(ok=True, value=cleaned, reason=None)


def is_blank(value: Any) -> bool:
    """True when value is None or whitespace-only string."""
    if value is None:
        return True
    return str(value).strip() == ""
