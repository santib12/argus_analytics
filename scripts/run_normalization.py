#!/usr/bin/env python3
"""
Phase 4 — Apply normalization to DB vendors and write a data-quality report.

Usage:
  source .venv/bin/activate
  python scripts/run_normalization.py
  python scripts/run_normalization.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config.logging import get_logger
from src.database.connection import check_connection, get_connection
from src.processing.normalize_names import normalize_company_name
from src.processing.validate import RejectLog, validate_uei

logger = get_logger(__name__)
PROCESSED_DIR = ROOT / "data" / "processed" / "vendors"
REPORT_PATH = ROOT / "docs" / "data_quality_report.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize vendor names and write DQ report")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute metrics and report without updating the database",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if not check_connection():
            logger.error("Database connection failed")
            return 1
    except Exception:
        logger.exception("Database connection failed")
        return 1

    rejects = RejectLog()
    updated = 0
    unchanged = 0
    uei_ok = 0
    uei_bad = 0
    null_uei = 0
    name_counts: Counter[str] = Counter()

    with get_connection() as conn:
        rows = conn.execute(
            text(
                """
                SELECT vendor_id, recipient_name, recipient_uei, normalized_name
                FROM vendors
                ORDER BY vendor_id
                """
            )
        ).mappings().all()

        for row in rows:
            vendor_id = row["vendor_id"]
            recipient_name = row["recipient_name"]
            new_normalized = normalize_company_name(recipient_name)

            if new_normalized:
                name_counts[new_normalized] += 1
            else:
                rejects.add(
                    entity="vendor",
                    key=str(vendor_id),
                    reason="name_blank_after_normalize",
                    raw=recipient_name,
                )

            uei_result = validate_uei(row["recipient_uei"])
            if uei_result.reason == "uei_missing":
                null_uei += 1
            elif not uei_result.ok:
                uei_bad += 1
                rejects.add(
                    entity="vendor",
                    key=str(vendor_id),
                    reason=uei_result.reason or "uei_invalid",
                    raw=row["recipient_uei"],
                )
            else:
                uei_ok += 1

            if new_normalized and new_normalized != row["normalized_name"]:
                if not args.dry_run:
                    conn.execute(
                        text(
                            """
                            UPDATE vendors
                            SET normalized_name = :normalized_name,
                                updated_at = NOW()
                            WHERE vendor_id = :vendor_id
                            """
                        ),
                        {
                            "normalized_name": new_normalized,
                            "vendor_id": vendor_id,
                        },
                    )
                updated += 1
            else:
                unchanged += 1

        if not args.dry_run:
            conn.commit()

    duplicate_names = {name: count for name, count in name_counts.items() if count > 1}

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    reject_path = PROCESSED_DIR / f"vendor_rejects_{stamp}.json"
    reject_path.write_text(
        json.dumps(rejects.entries, indent=2) + "\n",
        encoding="utf-8",
    )

    metrics = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "vendors_scanned": len(rows),
        "normalized_name_updated": updated,
        "normalized_name_unchanged": unchanged,
        "uei_ok": uei_ok,
        "uei_missing": null_uei,
        "uei_invalid": uei_bad,
        "reject_count": len(rejects),
        "duplicate_normalized_names": len(duplicate_names),
        "reject_log": str(reject_path.relative_to(ROOT)),
    }

    _write_report(metrics, duplicate_names)
    logger.info("Normalization complete: %s", metrics)
    logger.info("Data quality report -> %s", REPORT_PATH)
    return 0


def _write_report(metrics: dict, duplicate_names: dict[str, int]) -> None:
    dup_lines = "\n".join(
        f"- `{name}` × {count}" for name, count in sorted(duplicate_names.items())[:50]
    ) or "- (none)"

    body = f"""# Argus Data Quality Report

Generated: `{metrics["generated_at_utc"]}`  
Dry run: `{metrics["dry_run"]}`

> Raw files under `data/raw/` are never modified by Phase 4 tooling.

## Vendor metrics

| Metric | Value |
| --- | ---: |
| Vendors scanned | {metrics["vendors_scanned"]} |
| `normalized_name` updated | {metrics["normalized_name_updated"]} |
| `normalized_name` unchanged | {metrics["normalized_name_unchanged"]} |
| UEI OK | {metrics["uei_ok"]} |
| UEI missing | {metrics["uei_missing"]} |
| UEI invalid format | {metrics["uei_invalid"]} |
| Reject log entries | {metrics["reject_count"]} |
| Duplicate normalized names | {metrics["duplicate_normalized_names"]} |

## Reject log

Path: `{metrics["reject_log"]}`

## Duplicate normalized names (sample)

{dup_lines}

## Notes

- `normalize_company_name` uppercases names and canonicalizes LLC/INC/CORP-style suffixes.
- Invalid or missing UEIs are logged; rows are not deleted.
- Re-run: `python scripts/run_normalization.py`
"""
    REPORT_PATH.write_text(body, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
