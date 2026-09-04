"""Argus database package.

Phase 2: connection helpers + SQLAlchemy models.
Keep raw SQL schema as the source of truth in sql/schema.sql.
"""

from src.database.connection import check_connection, get_connection, get_engine
from src.database.models import (
    Agency,
    Award,
    Base,
    DojCase,
    EntityMatch,
    Exclusion,
    RiskFlag,
    RiskScore,
    Transaction,
    Vendor,
    VendorFeature,
)

__all__ = [
    "Agency",
    "Award",
    "Base",
    "DojCase",
    "EntityMatch",
    "Exclusion",
    "RiskFlag",
    "RiskScore",
    "Transaction",
    "Vendor",
    "VendorFeature",
    "check_connection",
    "get_connection",
    "get_engine",
]
