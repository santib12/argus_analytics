#!/usr/bin/env python3
"""
Phase 3 — CLI entrypoint for USAspending ingestion

Usage:
  source .venv/bin/activate
  python scripts/run_ingestion.py --max-award-pages 1
  python scripts/run_ingestion.py --awards-only --max-award-pages 1
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
        help="Not implemented yet (Phase 3 transactions scaffold).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    logger.info("Checking database connection...")
    if not check_connection():
        logger.error("Database connection failed")
        return 1

    if args.transactions_only:
        logger.error("Transaction ingestion is not implemented yet.")
        return 2

    award_stats = ingest_awards(
        max_pages=args.max_award_pages,
        limit=args.award_page_size,
    )
    logger.info("Award ingestion stats: %s", award_stats)

    if not args.awards_only:
        logger.info(
            "Skipping transactions for now. Re-run later after "
            "src/ingestion/usaspending_transactions.py is implemented."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
