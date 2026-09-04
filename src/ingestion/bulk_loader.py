"""
Phase 3 — Bulk / batch load helpers (SCAFFOLD)
==============================================

File: src/ingestion/bulk_loader.py

GOAL
----
Shared helpers for efficient PostgreSQL loads:
  - executemany / batch insert
  - upsert helpers
  - simple ingestion stats dataclass

Use these from awards/transactions modules so you don't duplicate SQL.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class IngestionStats:
    """Track counts for one ingestion run."""

    attempted: int = 0
    inserted: int = 0
    updated: int = 0
    skipped: int = 0
    failed: int = 0
    extras: dict = field(default_factory=dict)

    def merge(self, other: "IngestionStats") -> None:
        self.attempted += other.attempted
        self.inserted += other.inserted
        self.updated += other.updated
        self.skipped += other.skipped
        self.failed += other.failed


def upsert_many(conn, sql: str, rows: list[dict]) -> int:
    """
    Execute a parameterized upsert for many rows.

    TODO:
      if not rows:
          return 0
      result = conn.execute(text(sql), rows)  # or executemany style depending on SQLAlchemy version
      conn.commit()
      return len(rows)
    """
    raise NotImplementedError("Implement upsert_many")
