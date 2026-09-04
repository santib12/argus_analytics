"""
Phase 3 — USAspending awards ingestion
======================================

Fetch NASA FY2024 award pages, save raw JSON, transform, and upsert into PostgreSQL.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from sqlalchemy import text

from src.config.logging import get_logger
from src.database.connection import get_connection
from src.ingestion.usaspending_client import USASpendingClient

logger = get_logger(__name__)
RAW_DIR = Path("data/raw/usaspending")

NASA_NAME = "National Aeronautics and Space Administration"
# Common toptier code seen in USAspending generated ids / agency references
NASA_TOP_TIER_CODE = "080"


def build_nasa_fy2024_award_payload(page: int = 1, limit: int = 100) -> dict[str, Any]:
    """Build the MVP award-search payload for NASA FY2024 contracts."""
    return {
        "filters": {
            "award_type_codes": ["A", "B", "C", "D"],
            "time_period": [
                {
                    "start_date": "2023-10-01",
                    "end_date": "2024-09-30",
                }
            ],
            "agencies": [
                {
                    "type": "awarding",
                    "tier": "toptier",
                    "name": NASA_NAME,
                }
            ],
        },
        "fields": [
            "Award ID",
            "Recipient Name",
            "Recipient UEI",
            "Start Date",
            "End Date",
            "Award Amount",
            "Awarding Agency",
            "Awarding Sub Agency",
            "Contract Award Type",
            "Funding Agency",
            "Funding Sub Agency",
            "Description",
        ],
        "limit": limit,
        "page": page,
        "sort": "Award Amount",
        "order": "desc",
    }


def save_raw_awards_page(page: int, payload: dict[str, Any]) -> Path:
    """Persist one raw API response under data/raw/usaspending/."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = RAW_DIR / f"awards_page_{page:04d}_{timestamp}.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    logger.info("Saved raw awards page %s -> %s", page, path)
    return path


def _parse_date(value: Any) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    text_value = str(value)[:10]
    try:
        return date.fromisoformat(text_value)
    except ValueError:
        logger.warning("Could not parse date value: %r", value)
        return None


def _parse_money(value: Any) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        logger.warning("Could not parse money value: %r", value)
        return None


def _clean_uei(value: Any) -> str | None:
    if value is None:
        return None
    uei = str(value).strip().upper()
    if not uei:
        return None
    return uei[:12]


def transform_award_row(row: dict[str, Any]) -> dict[str, Any] | None:
    """Map one spending_by_award result into vendor/agency/award dicts."""
    award_id = row.get("generated_internal_id") or row.get("generated_unique_award_id")
    recipient_name = (row.get("Recipient Name") or "").strip()
    if not award_id or not recipient_name:
        logger.warning("Skipping award row missing award_id or recipient name: %r", row)
        return None

    awarding_name = (row.get("Awarding Agency") or NASA_NAME).strip()
    awarding_sub = (row.get("Awarding Sub Agency") or awarding_name).strip()
    funding_name = (row.get("Funding Agency") or awarding_name).strip()
    funding_sub = (row.get("Funding Sub Agency") or funding_name).strip()

    # Prefer a stable non-null agency_code so UNIQUE constraint upserts work.
    awarding_code = NASA_TOP_TIER_CODE if awarding_name == NASA_NAME else ""
    funding_code = NASA_TOP_TIER_CODE if funding_name == NASA_NAME else ""

    amount = _parse_money(row.get("Award Amount"))

    return {
        "vendor": {
            "recipient_uei": _clean_uei(row.get("Recipient UEI")),
            "recipient_name": recipient_name,
            "normalized_name": recipient_name.upper(),
            "city": None,
            "state": None,
            "country": None,
            "zip_code": None,
        },
        "awarding_agency": {
            "agency_code": awarding_code,
            "agency_name": awarding_name,
            "subtier_agency_name": awarding_sub,
        },
        "funding_agency": {
            "agency_code": funding_code,
            "agency_name": funding_name,
            "subtier_agency_name": funding_sub,
        },
        "award": {
            "award_id": str(award_id),
            "usaspending_internal_id": row.get("internal_id"),
            "award_type": row.get("Contract Award Type"),
            "description": row.get("Description"),
            "naics_code": None,
            "product_service_code": None,
            "start_date": _parse_date(row.get("Start Date")),
            "end_date": _parse_date(row.get("End Date")),
            "initial_value": amount,
            "current_value": amount,
            "potential_value": None,
            "place_of_performance_state": None,
            "set_aside_type": None,
        },
    }


def _upsert_vendor(conn, vendor: dict[str, Any]) -> int:
    uei = vendor.get("recipient_uei")
    if uei:
        vendor_id = conn.execute(
            text(
                """
                INSERT INTO vendors (
                    recipient_uei, recipient_name, normalized_name,
                    city, state, country, zip_code
                ) VALUES (
                    :recipient_uei, :recipient_name, :normalized_name,
                    :city, :state, :country, :zip_code
                )
                ON CONFLICT (recipient_uei) DO UPDATE SET
                    recipient_name = EXCLUDED.recipient_name,
                    normalized_name = EXCLUDED.normalized_name,
                    updated_at = NOW()
                RETURNING vendor_id
                """
            ),
            vendor,
        ).scalar_one()
        return int(vendor_id)

    # No UEI: reuse existing row with same normalized name when possible.
    existing = conn.execute(
        text(
            """
            SELECT vendor_id
            FROM vendors
            WHERE recipient_uei IS NULL
              AND normalized_name = :normalized_name
            ORDER BY vendor_id
            LIMIT 1
            """
        ),
        {"normalized_name": vendor["normalized_name"]},
    ).scalar()
    if existing is not None:
        return int(existing)

    vendor_id = conn.execute(
        text(
            """
            INSERT INTO vendors (
                recipient_uei, recipient_name, normalized_name,
                city, state, country, zip_code
            ) VALUES (
                NULL, :recipient_name, :normalized_name,
                :city, :state, :country, :zip_code
            )
            RETURNING vendor_id
            """
        ),
        vendor,
    ).scalar_one()
    return int(vendor_id)


def _upsert_agency(conn, agency: dict[str, Any]) -> int:
    agency_id = conn.execute(
        text(
            """
            INSERT INTO agencies (agency_code, agency_name, subtier_agency_name)
            VALUES (:agency_code, :agency_name, :subtier_agency_name)
            ON CONFLICT (agency_code, agency_name, subtier_agency_name)
            DO UPDATE SET agency_name = EXCLUDED.agency_name
            RETURNING agency_id
            """
        ),
        agency,
    ).scalar_one()
    return int(agency_id)


def _upsert_award(
    conn,
    award: dict[str, Any],
    vendor_id: int,
    awarding_agency_id: int,
    funding_agency_id: int,
) -> None:
    payload = {
        **award,
        "vendor_id": vendor_id,
        "awarding_agency_id": awarding_agency_id,
        "funding_agency_id": funding_agency_id,
    }
    conn.execute(
        text(
            """
            INSERT INTO awards (
                award_id, usaspending_internal_id, vendor_id,
                awarding_agency_id, funding_agency_id,
                award_type, description, naics_code, product_service_code,
                start_date, end_date,
                initial_value, current_value, potential_value,
                place_of_performance_state, set_aside_type
            ) VALUES (
                :award_id, :usaspending_internal_id, :vendor_id,
                :awarding_agency_id, :funding_agency_id,
                :award_type, :description, :naics_code, :product_service_code,
                :start_date, :end_date,
                :initial_value, :current_value, :potential_value,
                :place_of_performance_state, :set_aside_type
            )
            ON CONFLICT (award_id) DO UPDATE SET
                usaspending_internal_id = EXCLUDED.usaspending_internal_id,
                vendor_id = EXCLUDED.vendor_id,
                awarding_agency_id = EXCLUDED.awarding_agency_id,
                funding_agency_id = EXCLUDED.funding_agency_id,
                award_type = EXCLUDED.award_type,
                description = EXCLUDED.description,
                start_date = EXCLUDED.start_date,
                end_date = EXCLUDED.end_date,
                initial_value = EXCLUDED.initial_value,
                current_value = EXCLUDED.current_value,
                updated_at = NOW()
            """
        ),
        payload,
    )


def upsert_vendors_agencies_awards(rows: list[dict[str, Any]]) -> dict[str, int]:
    """Load transformed award rows into PostgreSQL. Returns count stats."""
    stats = {"vendors": 0, "agencies": 0, "awards": 0, "skipped": 0}
    if not rows:
        return stats

    with get_connection() as conn:
        for row in rows:
            if row is None:
                stats["skipped"] += 1
                continue
            try:
                vendor_id = _upsert_vendor(conn, row["vendor"])
                awarding_agency_id = _upsert_agency(conn, row["awarding_agency"])
                funding_agency_id = _upsert_agency(conn, row["funding_agency"])
                _upsert_award(
                    conn,
                    row["award"],
                    vendor_id=vendor_id,
                    awarding_agency_id=awarding_agency_id,
                    funding_agency_id=funding_agency_id,
                )
                stats["vendors"] += 1
                stats["agencies"] += 1
                stats["awards"] += 1
            except Exception:
                logger.exception("Failed to upsert award row: %s", row.get("award", {}))
                stats["skipped"] += 1
                conn.rollback()
                continue
        conn.commit()

    return stats


def ingest_awards(max_pages: int | None = None, limit: int = 100) -> dict[str, int]:
    """Fetch NASA FY2024 awards, save raw pages, and upsert into PostgreSQL."""
    stats = {"vendors": 0, "agencies": 0, "awards": 0, "skipped": 0, "pages": 0}
    base_payload = build_nasa_fy2024_award_payload(page=1, limit=limit)

    with USASpendingClient() as client:
        for page_num, page in enumerate(client.iter_award_pages(base_payload), start=1):
            save_raw_awards_page(page_num, page)
            results = page.get("results") or []
            transformed = [
                item
                for item in (transform_award_row(row) for row in results)
                if item is not None
            ]
            skipped_in_transform = len(results) - len(transformed)
            page_stats = upsert_vendors_agencies_awards(transformed)
            for key in ("vendors", "agencies", "awards", "skipped"):
                stats[key] += page_stats.get(key, 0)
            stats["skipped"] += skipped_in_transform
            stats["pages"] += 1
            logger.info("Ingested awards page %s: %s", page_num, page_stats)

            if max_pages is not None and page_num >= max_pages:
                break

    logger.info("Award ingestion complete: %s", stats)
    return stats
