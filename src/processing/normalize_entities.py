"""
Phase 4 — Entity / location normalization
=========================================

Normalize addresses, state codes, and agency display names lightly.
"""

from __future__ import annotations

import re
from typing import Any

from src.processing.normalize_names import normalize_whitespace

_WHITESPACE_RE = re.compile(r"\s+")

# Common full state names → USPS 2-letter (subset; extend as needed)
_STATE_NAMES: dict[str, str] = {
    "ALABAMA": "AL",
    "ALASKA": "AK",
    "ARIZONA": "AZ",
    "ARKANSAS": "AR",
    "CALIFORNIA": "CA",
    "COLORADO": "CO",
    "CONNECTICUT": "CT",
    "DELAWARE": "DE",
    "DISTRICT OF COLUMBIA": "DC",
    "FLORIDA": "FL",
    "GEORGIA": "GA",
    "HAWAII": "HI",
    "IDAHO": "ID",
    "ILLINOIS": "IL",
    "INDIANA": "IN",
    "IOWA": "IA",
    "KANSAS": "KS",
    "KENTUCKY": "KY",
    "LOUISIANA": "LA",
    "MAINE": "ME",
    "MARYLAND": "MD",
    "MASSACHUSETTS": "MA",
    "MICHIGAN": "MI",
    "MINNESOTA": "MN",
    "MISSISSIPPI": "MS",
    "MISSOURI": "MO",
    "MONTANA": "MT",
    "NEBRASKA": "NE",
    "NEVADA": "NV",
    "NEW HAMPSHIRE": "NH",
    "NEW JERSEY": "NJ",
    "NEW MEXICO": "NM",
    "NEW YORK": "NY",
    "NORTH CAROLINA": "NC",
    "NORTH DAKOTA": "ND",
    "OHIO": "OH",
    "OKLAHOMA": "OK",
    "OREGON": "OR",
    "PENNSYLVANIA": "PA",
    "RHODE ISLAND": "RI",
    "SOUTH CAROLINA": "SC",
    "SOUTH DAKOTA": "SD",
    "TENNESSEE": "TN",
    "TEXAS": "TX",
    "UTAH": "UT",
    "VERMONT": "VT",
    "VIRGINIA": "VA",
    "WASHINGTON": "WA",
    "WEST VIRGINIA": "WV",
    "WISCONSIN": "WI",
    "WYOMING": "WY",
}


def normalize_state(value: Any) -> str | None:
    """
    Normalize a US state to a 2-letter code when possible.

    Accepts 'CA', 'ca', 'California'. Unknown values return uppercase stripped
    text truncated to 2 only when already length 2; otherwise None.
    """
    if value is None:
        return None
    text = _WHITESPACE_RE.sub(" ", str(value).strip().upper())
    if not text:
        return None
    if len(text) == 2 and text.isalpha():
        return text
    return _STATE_NAMES.get(text)


def normalize_agency_name(value: Any) -> str | None:
    """Uppercase + collapse whitespace for agency display names."""
    text = normalize_whitespace(value)
    if text is None:
        return None
    return text.upper()


def normalize_city(value: Any) -> str | None:
    """Title-ish city cleanup: collapse whitespace, keep readable case via upper."""
    text = normalize_whitespace(value)
    if text is None:
        return None
    return text.upper()
