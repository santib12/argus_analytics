"""
Phase 3 — USAspending transactions ingestion (SCAFFOLD)
=======================================================

File: src/ingestion/usaspending_transactions.py
Depends on: usaspending_client.py, awards already loaded (or load jointly)

GOAL
----
For awards in scope (or each award_id), fetch transactions and upsert into
`transactions` table.

PREFERRED ENDPOINT FOR PER-AWARD HISTORY
---------------------------------------
POST /api/v2/transactions/
  body: {"award_id": <numeric internal id>, "page": 1, "limit": 100}

Also available:
POST /api/v2/search/spending_by_transaction/  (requires sort)

IMPORTANT
---------
- transaction_id must be stable (use API transaction id string)
- modification_number should stay TEXT
- action_date is required (DATE)
- Never assume SUM(transactions) == awards.current_value without care
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


def save_raw_transaction_page(
    award_internal_id: int,
    page: int,
    payload: dict[str, Any],
) -> Path:
    """Persist one raw transactions API response under data/raw/usaspending/."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = (
        RAW_DIR
        / f"transactions_award_{award_internal_id}_page_{page:04d}_{timestamp}.json"
    )
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    logger.info(
        "Saved raw transactions page %s for award_internal_id=%s -> %s",
        page,
        award_internal_id,
        path,
    )
    return path


def fetch_transactions_for_award(
    award_internal_id: int,
    page: int = 1,
    limit: int = 100,
    *,
    save_raw: bool = True,
    client: USASpendingClient | None = None,
) -> dict[str, Any]:
    """
    Fetch one page of transactions for a USAspending award.

    Parameters
    ----------
    award_internal_id:
        Numeric USAspending award id (awards.usaspending_internal_id),
        NOT the Argus text award_id (CONT_AWD_...).
    page:
        1-based page number.
    limit:
        Page size (API max is typically 100).
    save_raw:
        If True, write the response under data/raw/usaspending/.
    client:
        Optional shared USASpendingClient (caller owns lifecycle if provided).

    Returns
    -------
    Parsed JSON body with page_metadata + results.
    """
    if award_internal_id is None:
        raise ValueError("award_internal_id is required")

    payload: dict[str, Any] = {
        "award_id": int(award_internal_id),
        "page": page,
        "limit": limit,
    }

    owns_client = client is None
    if owns_client:
        client = USASpendingClient()

    assert client is not None
    try:
        logger.info(
            "Fetching transactions award_internal_id=%s page=%s limit=%s",
            award_internal_id,
            page,
            limit,
        )
        data = client.post_json("/api/v2/transactions/", payload)
    finally:
        if owns_client:
            client.close()

    if save_raw:
        save_raw_transaction_page(int(award_internal_id), page, data)

    return data


def _parse_date(value: Any) -> date | None:
    """Convert an API date value into a date, or None if missing/invalid."""
    if value is None or value == "":
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    text_value = str(value)[:10]
    try:
        return date.fromisoformat(text_value)
    except ValueError:
        return None


def _parse_money(value: Any) -> Decimal | None:
    """Convert an API money value into Decimal, or None if missing/invalid."""
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def transform_transaction_row(
    row: dict[str, Any],
    award_id: str,
    vendor_id: int | None,
    agency_id: int | None,
) -> dict[str, Any] | None:
    """
    Map one USAspending transaction JSON object into one Argus
    `transactions` table dictionary. Does not write to the database.
    """
    # Stable source primary key from USAspending
    raw_id = row.get("id")
    if raw_id is None:
        return None
    transaction_id = str(raw_id).strip()
    if not transaction_id:
        return None

    # Required FK parent (Argus awards.award_id)
    if award_id is None or not str(award_id).strip():
        return None
    cleaned_award_id = str(award_id).strip()

    # Required action_date (DATE NOT NULL)
    action_date = _parse_date(row.get("action_date"))
    if action_date is None:
        return None

    federal_action_obligation = _parse_money(row.get("federal_action_obligation"))
    current_total_value = _parse_money(row.get("current_total_value"))
    potential_total_value = _parse_money(row.get("potential_total_value"))

    mod = row.get("modification_number")
    if mod is None or mod == "":
        modification_number = None
    else:
        modification_number = str(mod)

    description = row.get("description")
    if description is not None:
        description = str(description).strip() or None

    return {
        "transaction_id": transaction_id,
        "award_id": cleaned_award_id,
        "vendor_id": vendor_id,
        "agency_id": agency_id,
        "action_date": action_date,
        "federal_action_obligation": federal_action_obligation,
        "current_total_value": current_total_value,
        "potential_total_value": potential_total_value,
        "modification_number": modification_number,
        "description": description,
    }


def upsert_transactions(rows: list[dict[str, Any] | None]) -> dict[str, int]:
    """
    Upsert transformed transaction rows into PostgreSQL.

    Uses ON CONFLICT (transaction_id) DO UPDATE so re-runs are idempotent
    and refresh mutable fields (dates, obligations, description, etc.).

    Returns counts: upserted, skipped.
    """
    stats = {"upserted": 0, "skipped": 0}
    if not rows:
        return stats

    with get_connection() as conn:
        for row in rows:
            if row is None:
                stats["skipped"] += 1
                continue
            try:
                conn.execute(
                    text(
                        """
                        INSERT INTO transactions (
                            transaction_id,
                            award_id,
                            vendor_id,
                            agency_id,
                            action_date,
                            federal_action_obligation,
                            current_total_value,
                            potential_total_value,
                            modification_number,
                            description
                        ) VALUES (
                            :transaction_id,
                            :award_id,
                            :vendor_id,
                            :agency_id,
                            :action_date,
                            :federal_action_obligation,
                            :current_total_value,
                            :potential_total_value,
                            :modification_number,
                            :description
                        )
                        ON CONFLICT (transaction_id) DO UPDATE SET
                            award_id = EXCLUDED.award_id,
                            vendor_id = EXCLUDED.vendor_id,
                            agency_id = EXCLUDED.agency_id,
                            action_date = EXCLUDED.action_date,
                            federal_action_obligation = EXCLUDED.federal_action_obligation,
                            current_total_value = EXCLUDED.current_total_value,
                            potential_total_value = EXCLUDED.potential_total_value,
                            modification_number = EXCLUDED.modification_number,
                            description = EXCLUDED.description
                        """
                    ),
                    row,
                )
                stats["upserted"] += 1
            except Exception:
                logger.exception(
                    "Failed to upsert transaction_id=%s",
                    row.get("transaction_id"),
                )
                stats["skipped"] += 1
                conn.rollback()
                continue
        conn.commit()

    return stats


def ingest_transactions_for_loaded_awards(
    limit_awards: int | None = None,
    page_size: int = 100,
    max_pages_per_award: int | None = None,
) -> dict[str, int]:
    """
    For awards already in PostgreSQL, fetch all transaction pages and upsert.

    Skips awards with NULL usaspending_internal_id (cannot call the API).
    Continues to the next award if one award's API/transform path fails.
    """
    stats = {
        "awards_considered": 0,
        "awards_processed": 0,
        "awards_skipped": 0,
        "pages": 0,
        "upserted": 0,
        "skipped": 0,
    }

    sql = """
        SELECT
            award_id,
            usaspending_internal_id,
            vendor_id,
            awarding_agency_id
        FROM awards
        WHERE usaspending_internal_id IS NOT NULL
        ORDER BY award_id
    """
    if limit_awards is not None:
        sql += " LIMIT :limit_awards"

    with get_connection() as conn:
        if limit_awards is not None:
            award_rows = (
                conn.execute(text(sql), {"limit_awards": limit_awards}).mappings().all()
            )
        else:
            award_rows = conn.execute(text(sql)).mappings().all()

    stats["awards_considered"] = len(award_rows)
    if not award_rows:
        logger.warning("No awards with usaspending_internal_id found; nothing to ingest")
        return stats

    with USASpendingClient() as client:
        for award in award_rows:
            award_id = award["award_id"]
            internal_id = award["usaspending_internal_id"]
            vendor_id = award["vendor_id"]
            agency_id = award["awarding_agency_id"]

            try:
                page = 1
                while True:
                    if max_pages_per_award is not None and page > max_pages_per_award:
                        break

                    data = fetch_transactions_for_award(
                        int(internal_id),
                        page=page,
                        limit=page_size,
                        save_raw=True,
                        client=client,
                    )
                    stats["pages"] += 1

                    results = data.get("results") or []
                    if not results:
                        break

                    transformed: list[dict[str, Any] | None] = [
                        transform_transaction_row(
                            row,
                            award_id=str(award_id),
                            vendor_id=vendor_id,
                            agency_id=agency_id,
                        )
                        for row in results
                    ]
                    page_stats = upsert_transactions(transformed)
                    stats["upserted"] += page_stats["upserted"]
                    stats["skipped"] += page_stats["skipped"]

                    page_metadata = data.get("page_metadata") or {}
                    has_next = page_metadata.get("hasNext")
                    if has_next is False:
                        break
                    if has_next is None and len(results) < page_size:
                        break

                    page += 1

                stats["awards_processed"] += 1
                logger.info(
                    "Finished transactions for award_id=%s internal_id=%s",
                    award_id,
                    internal_id,
                )
            except Exception:
                logger.exception(
                    "Failed transaction ingestion for award_id=%s internal_id=%s",
                    award_id,
                    internal_id,
                )
                stats["awards_skipped"] += 1
                continue

    logger.info("Transaction ingestion complete: %s", stats)
    return stats
