#!/usr/bin/env python3
"""
Phase 3 — CLI entrypoint for USAspending ingestion

Usage:
  source .venv/bin/activate
  python scripts/run_ingestion.py --max-award-pages 1
  python scripts/run_ingestion.py --awards-only --max-award-pages 1
  python scripts/run_ingestion.py --transactions-only --limit-awards 1
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config.logging import get_logger
from src.database.connection import check_connection
from src.ingestion.usaspending_awards import ingest_awards
from src.ingestion.usaspending_transactions import ingest_transactions_for_loaded_awards

logger = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Argus USAspending ingestion (NASA FY2024 MVP)"
    )
    parser.add_argument("--max-award-pages", type=int, default=None)
    parser.add_argument("--award-page-size", type=int, default=100)
    parser.add_argument("--awards-only", action="store_true")
    parser.add_argument(
        "--transactions-only",
        action="store_true",
        help="Skip awards; ingest transactions for awards already in the DB.",
    )
    parser.add_argument(
        "--limit-awards",
        type=int,
        default=None,
        help="Max awards to process during transaction ingestion.",
    )
    parser.add_argument(
        "--transaction-page-size",
        type=int,
        default=100,
        help="Page size for POST /api/v2/transactions/.",
    )
    parser.add_argument(
        "--max-transaction-pages",
        type=int,
        default=None,
        help="Optional cap on transaction pages fetched per award.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    logger.info("Checking database connection...")
    try:
        if not check_connection():
            logger.error("Database connection failed")
            return 1
    except Exception:
        logger.exception("Database connection failed")
        return 1

    if not args.transactions_only:
        award_stats = ingest_awards(
            max_pages=args.max_award_pages,
            limit=args.award_page_size,
        )
        logger.info("Award ingestion stats: %s", award_stats)

    if not args.awards_only:
        tx_stats = ingest_transactions_for_loaded_awards(
            limit_awards=args.limit_awards,
            page_size=args.transaction_page_size,
            max_pages_per_award=args.max_transaction_pages,
        )
        logger.info("Transaction ingestion stats: %s", tx_stats)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
