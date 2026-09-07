"""Phase 4 — unit tests for normalization helpers."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from src.processing.normalize_awards import normalize_code, normalize_date, normalize_money
from src.processing.normalize_entities import normalize_agency_name, normalize_state
from src.processing.normalize_names import normalize_company_name
from src.processing.validate import validate_uei


def test_normalize_company_name_llc_variant():
    # ARRANGE
    raw = "ACME TECHNOLOGIES, L.L.C."

    # ACT
    result = normalize_company_name(raw)

    # ASSERT
    assert result == "ACME TECHNOLOGIES LLC"


def test_normalize_company_name_inc_and_whitespace():
    assert normalize_company_name("  Foo   Bar, Inc.  ") == "FOO BAR INC"


def test_normalize_company_name_blank_is_none():
    assert normalize_company_name(None) is None
    assert normalize_company_name("   ") is None


def test_normalize_date_iso():
    assert normalize_date("2024-03-15") == date(2024, 3, 15)
    assert normalize_date("") is None
    assert normalize_date("not-a-date") is None


def test_normalize_money():
    assert normalize_money("1,378,971.52") == Decimal("1378971.52")
    assert normalize_money(0) == Decimal("0")
    assert normalize_money(None) is None


def test_normalize_code():
    assert normalize_code("  ab12  ", max_len=4) == "AB12"
    assert normalize_code("") is None


def test_normalize_state():
    assert normalize_state("ca") == "CA"
    assert normalize_state("California") == "CA"
    assert normalize_state(None) is None


def test_normalize_agency_name():
    assert normalize_agency_name("  National Aeronautics  ") == "NATIONAL AERONAUTICS"


def test_validate_uei_ok():
    result = validate_uei("abcDEF123456")
    assert result.ok is True
    assert result.value == "ABCDEF123456"


def test_validate_uei_bad():
    assert validate_uei(None).reason == "uei_missing"
    assert validate_uei("TOO_SHORT").ok is False
    assert validate_uei("INVALID!!!!").ok is False
