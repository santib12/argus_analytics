# Argus Architecture (Draft)

Status: Phase 2 complete — schema + connection layer ready for ingestion.

## Purpose

Argus turns public federal procurement data into **explainable investigative signals**.

```text
HIGH RISK ≠ FRAUD
ANOMALY ≠ MISCONDUCT
```

## Current MVP Scope

- Agency: National Aeronautics and Space Administration (NASA)
- Fiscal year: FY2024 (`2023-10-01` → `2024-09-30`)
- Award types: contracts `A/B/C/D`

## High-Level Flow

```text
USAspending / SAM / DOJ (public)
        ↓
Python ingestion (Phase 3+)
        ↓
Normalization (Phase 4)
        ↓
PostgreSQL (Phase 2)
        ↓
SQL / Rules / Stats / ML / Graph
        ↓
Risk scores
        ↓
FastAPI + Power BI + GenAI summaries
```

## Database Design Decisions (Phase 2)

| Decision | Choice | Why |
|---|---|---|
| Award PK | `generated_unique_award_id` as `awards.award_id` | Stable natural key across USAspending |
| Extra award id | `usaspending_internal_id` | Convenient for API detail fetches |
| Vendor PK | Internal `vendor_id` | Names collide; UEI is unique when present |
| Money types | `NUMERIC(20,2)` | Avoid float rounding issues |
| Analytics history | `analysis_date` on features/scores | Re-runnable analyses without overwrite confusion |
| Risk outputs | flags/scores tables | Indicators only — not guilt determinations |

## Core Tables

- `vendors`, `agencies`, `awards`, `transactions` — transactional core
- `exclusions`, `entity_matches` — compliance matching (Phases 7–8)
- `vendor_features`, `risk_flags`, `risk_scores` — analytics outputs
- `doj_cases` — retrospective case studies (Phase 14)

## Python Access

- Settings: `src/config/settings.py` (from `.env`)
- Connection: `src/database/connection.py` (`get_engine`, `check_connection`)
- ORM models: `src/database/models.py` (mirror of `sql/schema.sql`)

## Local Setup Commands

```bash
# apply schema/indexes/views
./scripts/init_db.sh

# verify Python connectivity
source .venv/bin/activate
python -c "from src.database.connection import check_connection; print(check_connection())"
```

## Next Phase

Phase 3 — USAspending ingestion for NASA FY2024 into these tables.
