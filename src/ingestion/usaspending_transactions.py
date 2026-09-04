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

# TODO imports similar to usaspending_awards.py


def fetch_transactions_for_award(award_internal_id: int, page: int = 1, limit: int = 100) -> dict:
    """
    TODO: call POST /api/v2/transactions/ with award_id=award_internal_id.
    Save raw response under data/raw/usaspending/transactions_*.json.
    """
    raise NotImplementedError("Implement fetch_transactions_for_award")


def transform_transaction_row(row: dict, award_id: str, vendor_id: int | None, agency_id: int | None) -> dict:
    """
    TODO: map API transaction object -> transactions table columns.
    """
    raise NotImplementedError("Implement transform_transaction_row")


def upsert_transactions(rows: list[dict]) -> dict:
    """
    TODO: INSERT ... ON CONFLICT (transaction_id) DO UPDATE / DO NOTHING.
    Return counts inserted/updated/skipped.
    """
    raise NotImplementedError("Implement upsert_transactions")


def ingest_transactions_for_loaded_awards(limit_awards: int | None = None) -> dict:
    """
    TODO orchestration:
      1) SELECT award_id, usaspending_internal_id, vendor_id, awarding_agency_id FROM awards
      2) for each award with internal id, paginate transactions
      3) transform + upsert
      4) return stats
    """
    raise NotImplementedError("Implement ingest_transactions_for_loaded_awards")
