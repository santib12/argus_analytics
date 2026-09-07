# Argus Development Progress

## Project

**Argus — Federal Procurement Risk & Forensic Analytics**

Repository:

https://github.com/santib12/argus_analytics

---

# Progress Snapshot

```text
Current Phase:              Phase 5 — Core SQL Investigations
Overall Status:             Phase 4 COMPLETE for core normalizers/tests; full roadmap ~35%; MVP ~50%
Last Reviewed:              2026-09-07
Primary Working Component:  Phase 4 processing normalizers + run_normalization.py
Primary Blocker:            None (run normalization against local Postgres when available)
Recommended Next Task:      Phase 5 — first SQL investigation scripts under sql/analysis/
```

---

# Overall Progress

Statuses are based on **code inspection + runnable checks in this review**, not README checkboxes alone.

| Phase | Status | Progress | Evidence |
| ----- | ------ | -------: | -------- |
| Phase 0 — Repository and Development Environment | COMPLETE | 100% | `.gitignore`, `.env.example`, `src/config/`, `requirements.txt`, `pyproject.toml`, `LICENSE`, venv present; `.env` ignored |
| Phase 1 — Understand the Data | COMPLETE | 100% | `docs/data_dictionary.md`, `docs/sources_notes.md`, `data/samples/usaspending/*`, `notebooks/01_data_exploration.ipynb`, provenance recorded |
| Phase 2 — PostgreSQL Database | COMPLETE | 90% | Schema/indexes/models/connection/`init_db.sh`; views still stub |
| Phase 3 — USAspending Data Ingestion | COMPLETE | 90% | Awards + transactions fetch/transform/upsert/CLI verified live (100 txs / 1 award page); larger full-FY pull and pytest coverage still open; `bulk_loader.upsert_many` still stub |
| Phase 4 — Data Cleaning and Normalization | COMPLETE | 90% | `normalize_*` + `validate_uei` + tests (10 passed); `run_normalization.py` + DQ report template; award ingest uses `normalize_company_name`; local DB backfill when Postgres is up |
| Phase 5 — Core SQL Investigations | NOT STARTED | 0% | `sql/analysis/` empty; `sql/views.sql` is a stub `SELECT` |
| Phase 6 — Rules-Based Forensic Analytics | NOT STARTED | 0% | `src/analytics/rules/` empty |
| Phase 7 — SAM.gov Exclusion Integration | NOT STARTED | 0% | No SAM client/loader; `exclusions` table schema only |
| Phase 8 — Entity Resolution Implementation | NOT STARTED | 0% | `src/entity_resolution/` empty |
| Phase 9 — Statistical Analytics Implementation | NOT STARTED | 0% | `src/analytics/statistics/` empty |
| Phase 10 — Feature Engineering | NOT STARTED | 0% | `vendor_features` table schema only; no feature builders |
| Phase 11 — Machine-Learning Anomaly Detection | NOT STARTED | 0% | `src/analytics/ml/` empty (`scikit-learn` listed in requirements only) |
| Phase 12 — Graph Analytics Implementation | NOT STARTED | 0% | `src/analytics/graph/` empty (`networkx` listed in requirements only) |
| Phase 13 — Argus Risk Score | NOT STARTED | 0% | `src/scoring/` empty; `risk_scores` table schema only |
| Phase 14 — DOJ Retrospective Case Studies | NOT STARTED | 0% | `docs/case_studies/.gitkeep` only; `doj_cases` table schema only |
| Phase 15 — FastAPI Backend | NOT STARTED | 0% | `src/api/routes/` empty; FastAPI in requirements only |
| Phase 16 — Power BI Dashboard | NOT STARTED | 0% | `powerbi/.gitkeep` + empty `screenshots/`; no `.pbix` or connection docs |
| Phase 17 — GenAI Investigation Summaries | NOT STARTED | 0% | `src/genai/` empty |
| Phase 18 — Testing | NOT STARTED | 0% | `tests/__init__.py` only; `pytest` runs zero tests |
| Phase 19 — Docker | NOT STARTED | 0% | No `Dockerfile` / `docker-compose.yml` |
| Phase 20 — Cloud Deployment | NOT STARTED | 0% | No cloud config/deploy assets |
| Phase 21 — Documentation | IN PROGRESS | 25% | Strong README + Phase 1–2 docs; missing ops runbooks, API docs, rule methodology docs |
| Phase 22 — Portfolio Release | NOT STARTED | 0% | Not at release gate |

**README vs reality:** README marks Phases 0–4 complete; Phase 5 is next. Matches verified ingest + normalization modules/tests.

---

# Completed Work

- [x] **Repository / environment (Phase 0)**
  - Files: `.gitignore`, `.env.example`, `requirements.txt`, `pyproject.toml`, `LICENSE`, `src/config/settings.py`, `src/config/logging.py`
  - Verified by: `git check-ignore -v .env`; imports of settings; directory scaffold present
  - Current capability: local config/logging without committing secrets

- [x] **Data research package (Phase 1)**
  - Files: `docs/data_dictionary.md`, `docs/sources_notes.md`, `data/samples/usaspending/*`, `notebooks/01_data_exploration.ipynb`
  - Verified by: files tracked in git; MVP scope locked to NASA FY2024 contracts A/B/C/D in `docs/sources_notes.md`
  - Current capability: documented entities/keys and small reproducible samples

- [x] **PostgreSQL schema + indexes (Phase 2)**
  - Files: `sql/schema.sql`, `sql/indexes.sql`, `scripts/init_db.sh`
  - Verified by: file inspection (10 tables with FKs/constraints); indexes defined for core join paths
  - Current capability: schema ready to apply; `sql/views.sql` intentionally stubbed

- [x] **SQLAlchemy models + connection helpers (Phase 2)**
  - Files: `src/database/models.py`, `src/database/connection.py`, `src/database/__init__.py`
  - Verified by: `python -m compileall` + successful imports of models/settings
  - Current capability: typed ORM mirrors + `get_engine` / `get_connection` / `check_connection`

- [x] **Architecture notes (Phase 2)**
  - File: `docs/architecture.md`
  - Verified by: file present; documents MVP scope and design decisions

- [x] **USAspending HTTP client (Phase 3)**
  - File: `src/ingestion/usaspending_client.py`
  - Verified by: live POST 200 during transaction ingest; retries/timeout/`iter_award_pages`
  - Current capability: POST/GET JSON with retries; award page iteration helper

- [x] **Awards ingestion path (Phase 3)**
  - File: `src/ingestion/usaspending_awards.py`
  - Verified by: prior live award ingest + CLI
  - Current capability: NASA FY2024 payload, raw page save, transform, vendor/agency/award upserts

- [x] **Transaction ingestion path (Phase 3)**
  - File: `src/ingestion/usaspending_transactions.py`
  - Verified by: `python scripts/run_ingestion.py --transactions-only --limit-awards 1 --max-transaction-pages 1` → 100 upserted; `SELECT COUNT(*) FROM transactions` = 100; sample rows match `CONT_TX_...` ids
  - Current capability: fetch one/all pages per award, raw save, transform, upsert, orchestration

- [x] **Ingestion CLI (awards + transactions)**
  - File: `scripts/run_ingestion.py`
  - Verified by: `--transactions-only`, `--limit-awards`, `--max-transaction-pages` live run
  - Current capability: awards and/or transactions pipelines

---

# Work In Progress

- [ ] **Shared bulk upsert helper**
  - Current state: `IngestionStats` dataclass exists; `upsert_many` raises `NotImplementedError`
  - Missing: batch executemany/upsert implementation and adoption by awards/transactions
  - File: `src/ingestion/bulk_loader.py`

- [ ] **Investigator SQL views**
  - Current state: stub status `SELECT` only
  - Missing: real `CREATE VIEW` objects
  - File: `sql/views.sql`
  - Depends on: Phase 5 query design

- [ ] **Larger-scope Phase 3 soak**
  - Current state: small slice verified (1 award, 1 page)
  - Missing: multi-award / multi-page full NASA FY2024 pull and UI spot-check

- [ ] **Documentation depth (Phase 21 early)**
  - Current state: README roadmap + Phase 1/2 docs + PROGRESS.md
  - Missing: ingestion runbook, rule methodology, API docs, dashboard docs

---

# Not Started

Major planned areas with no meaningful implementation beyond empty directories or schema placeholders:

- Data cleaning / normalization (`src/processing/`)
- SQL investigation scripts (`sql/analysis/`)
- Rules engine (`src/analytics/rules/`)
- SAM.gov exclusion ingestion
- Entity resolution (`src/entity_resolution/`)
- Statistical analytics / ML / graph modules
- Risk scoring (`src/scoring/`)
- DOJ case study content (`docs/case_studies/`)
- FastAPI app (`src/api/`)
- Power BI artifacts (`powerbi/`)
- GenAI summaries (`src/genai/`)
- Automated test suite (`tests/` beyond empty package)
- Docker / cloud deployment

---

# Blockers

No known blockers for starting Phase 4 on the developer machine where Postgres and USAspending API are reachable.

### Remaining quality gaps (not hard blockers)

### No automated tests

Impact:
Regressions in client/transform/upsert cannot be caught by CI or `pytest`.

Affected:
Phase 3 quality gate, Phase 18

Required Action:
Add unit tests for transform helpers and mocked HTTP pagination.

---

# Repository Structure Status

```text
src/
├── config/                 COMPLETE
├── database/               COMPLETE (views SQL separate; live DB verify blocked this session)
├── ingestion/              COMPLETE for MVP path (bulk_loader.upsert_many still stub)
├── processing/             COMPLETE (core Phase 4 normalizers + validate)
├── entity_resolution/      NOT STARTED (empty)
├── analytics/
│   ├── rules/              NOT STARTED (empty)
│   ├── statistics/         NOT STARTED (empty)
│   ├── ml/                 NOT STARTED (empty)
│   └── graph/              NOT STARTED (empty)
├── scoring/                NOT STARTED (empty)
├── api/                    NOT STARTED (routes empty)
└── genai/                  NOT STARTED (empty)

sql/
├── schema.sql              COMPLETE
├── indexes.sql             COMPLETE
├── views.sql               IN PROGRESS (stub)
└── analysis/               NOT STARTED (empty)

scripts/
├── init_db.sh              COMPLETE (script present)
└── run_ingestion.py        IN PROGRESS (awards only)

docs/
├── data_dictionary.md      COMPLETE (Phase 1)
├── sources_notes.md        COMPLETE (Phase 1)
├── architecture.md         COMPLETE (Phase 2 draft)
└── case_studies/           NOT STARTED

data/
├── samples/usaspending/    COMPLETE (tracked samples)
├── raw/                    IN PROGRESS (ignored dumps; local awards page artifact present)
└── processed/              NOT STARTED (placeholders only)

tests/                      NOT STARTED
notebooks/                  IN PROGRESS (one exploration notebook)
powerbi/                    NOT STARTED
```

---

# Tests and Verification

| Check | Command | Result |
| ----- | ------- | ------ |
| Unit tests | `pytest` | FAIL / empty — exit code 5, **no tests ran** |
| Compilation | `python -m compileall -q src scripts` | PASS (prior) |
| Transaction transform (sample) | offline sample row transform | PASS |
| Live transaction ingest | `run_ingestion.py --transactions-only --limit-awards 1 --max-transaction-pages 1` | PASS (developer machine 2026-09-06) — 100 upserted |
| DB row count | `SELECT COUNT(*) FROM transactions` | PASS — 100 |
| `.env` ignored | `git check-ignore -v .env` | PASS |
| Raw dumps ignored | `git check-ignore` on `data/raw/usaspending/*.json` | PASS |
| Ruff / Black / Mypy | — | NOT CONFIGURED |
| Docker artifacts | `Dockerfile` / `docker-compose.yml` | ABSENT |

---

# Current Data Sources

## USAspending

```text
Status: COMPLETE for MVP slice (larger soak optional)
Implemented:
  - Documented endpoints/scope in docs/sources_notes.md
  - Tracked samples + provenance under data/samples/usaspending/
  - Reusable client (timeout, retries, award pagination helper)
  - Awards fetch/transform/upsert for NASA FY2024 contracts
  - Transactions fetch/paginate/transform/upsert for loaded awards
  - Raw awards + transactions persistence under data/raw/usaspending/ (gitignored)
  - CLI awards and transactions paths in scripts/run_ingestion.py
Missing:
  - Larger multi-award / multi-page soak as a formal checklist item
  - Automated pytest coverage
  - Bulk loader reuse (bulk_loader.upsert_many still stub)
```

## SAM.gov

```text
Status: NOT STARTED
Implemented:
  - Research notes in docs/sources_notes.md / data dictionary mentions
  - exclusions table in sql/schema.sql
  - SAM_API_KEY placeholder in .env.example
Missing:
  - Client, download/parse, load, active-vs-terminated handling, tests
```

## DOJ

```text
Status: NOT STARTED
Implemented:
  - doj_cases table schema
  - empty docs/case_studies/ placeholder
Missing:
  - Case research content, datasets, retrospective validation code
```

---

# Current Database State

```text
Database engine:            PostgreSQL (intended; local service not reachable this review)
Connection implementation:  SQLAlchemy Engine via DATABASE_URL (src/database/connection.py)
Schema:                     sql/schema.sql (source of truth)
Tables implemented (DDL):   vendors, agencies, awards, transactions, exclusions,
                            entity_matches, vendor_features, risk_flags, risk_scores, doj_cases
Indexes:                    sql/indexes.sql present for core FK/filter columns
Migrations:                 none (manual SQL apply via scripts/init_db.sh / psql)
Seed/sample data:           JSON/CSV samples in data/samples/ (not SQL seeds)
ORM models:                 src/database/models.py mirrors schema
Views:                      stub only (sql/views.sql)
Database verification:      BLOCKED this session (Postgres not accepting connections)
```

### Table implementation classification

| Table | Classification |
| ----- | -------------- |
| vendors | implemented (DDL + awards upsert path) |
| agencies | implemented (DDL + awards upsert path) |
| awards | implemented (DDL + awards upsert path) |
| transactions | partially implemented (DDL only; no loader) |
| exclusions | planned only beyond DDL |
| entity_matches | planned only beyond DDL |
| vendor_features | planned only beyond DDL |
| risk_flags | planned only beyond DDL |
| risk_scores | planned only beyond DDL |
| doj_cases | planned only beyond DDL |

---

# Current Analytics Capabilities

## SQL Analytics

```text
Status: NOT STARTED
Implemented: none under sql/analysis/; views stub only
Missing: vendor totals, growth, concentration, modifications, velocity, peer comparisons
Relevant files: sql/analysis/ (empty), sql/views.sql (stub)
```

## Rules Engine

```text
Status: NOT STARTED
Implemented: none
Missing: rapid growth, modification ratio, agency concentration, clustered awards,
         award velocity, modification frequency, SAM exclusion match; persistence to risk_flags
Relevant files: src/analytics/rules/ (empty)
```

## Statistical Analytics

```text
Status: NOT STARTED
Implemented: none (scipy/numpy dependencies only)
Missing: percentiles, z-scores, IQR, MAD, peer-group comparisons
Relevant files: src/analytics/statistics/ (empty)
```

## Feature Engineering

```text
Status: NOT STARTED
Implemented: vendor_features columns reserved in schema/models
Missing: feature computation pipeline and persistence
Relevant files: sql/schema.sql, src/database/models.py
```

## Machine Learning

```text
Status: NOT STARTED
Implemented: none (scikit-learn in requirements only)
Missing: Isolation Forest, preprocessing, training, scoring, model persistence
Relevant files: src/analytics/ml/ (empty), models/ (.gitkeep only)
```

## Graph Analytics

```text
Status: NOT STARTED
Implemented: none (networkx in requirements only)
Missing: vendor/agency graph, degrees, centrality, communities
Relevant files: src/analytics/graph/ (empty)
```

## Entity Resolution

```text
Status: NOT STARTED
Implemented: entity_matches DDL only
Missing: matching logic, review workflow, rapidfuzz usage in code
Relevant files: src/entity_resolution/ (empty)
```

## Risk Scoring

```text
Status: NOT STARTED
Implemented: risk_scores / risk_flags DDL only
Missing: weighted overall score, documented methodology, writers into DB
Relevant files: src/scoring/ (empty)
```

---

# Current Application Capabilities

## FastAPI

```text
Status: NOT STARTED
Evidence: src/api/routes/ empty; fastapi/uvicorn listed in requirements.txt only
```

## Power BI

```text
Status: NOT STARTED
Evidence: powerbi/.gitkeep and powerbi/screenshots/.gitkeep only; no dashboard artifacts
```

## GenAI

```text
Status: NOT STARTED
Evidence: src/genai/ empty; OPENAI_API_KEY placeholder only
```

## Docker

```text
Status: NOT STARTED
Evidence: no Dockerfile or docker-compose.yml
```

## Cloud

```text
Status: NOT STARTED
Evidence: no cloud deployment assets or runbooks
```

---

# Technical Debt

| Priority | Issue | Evidence |
| -------- | ----- | -------- |
| HIGH | No automated tests for ingestion/transform/DB | `tests/` empty; `pytest` exit 5 |
| HIGH | Awards upsert is row-by-row in a Python loop | `upsert_vendors_agencies_awards` in `usaspending_awards.py`; `bulk_loader.upsert_many` unimplemented |
| MEDIUM | `check_connection()` documents bool return but re-raises on failure | `src/database/connection.py` `except` → `raise` |
| MEDIUM | Settings default DB URL still uses `postgres:password` while `.env.example` uses `argus:password` | `src/config/settings.py` vs `.env.example` |
| MEDIUM | Award transform leaves many investigative fields null (NAICS, PSC, POP, set-aside, location) | `transform_award_row` hardcoded `None`s; list endpoint fields limited |
| MEDIUM | Agency code heuristic (`080` / empty string) may collide or under-specify subtiers | `usaspending_awards.py` |
| MEDIUM | README Phase 3 checklist was stale | Updated 2026-09-06; keep PROGRESS.md in sync after milestones |
| LOW | `sql/views.sql` stub prints status row instead of views | `sql/views.sql` |
| LOW | Dependencies listed early (ML/graph/FastAPI/openai) before corresponding modules exist | `requirements.txt` |
| LOW | Architecture doc still says “Phase 2 complete — ready for ingestion” while awards path already exists | `docs/architecture.md` |

---

# Known Bugs / Issues

### `check_connection` raises instead of returning `False`

**Severity:** MEDIUM

**File:** `src/database/connection.py`

**Problem:** Docstring says return `True` if `SELECT 1` succeeds, but exceptions are logged and re-raised.

**Expected behavior:** Return `False` on connection failure (or raise a dedicated error consistently and update callers).

**Current behavior:** Callers that treat it as a boolean gate (e.g. `scripts/run_ingestion.py`) never reach the `False` branch; process crashes with stack trace.

**Recommended fix:** Return `False` after logging, or change CLI to catch `OperationalError` explicitly.

### Live services unavailable in this review (environment, not necessarily code)

**Severity:** MEDIUM (process / environment)

**Problem:** PostgreSQL connection refused; USAspending DNS failure during audit.

**Expected behavior:** With Postgres running and network available, awards ingest should be re-verifiable.

**Current behavior:** End-to-end verification blocked this session.

**Recommended fix:** Start Postgres; re-run `check_connection` and `python scripts/run_ingestion.py --awards-only --max-award-pages 1`.

No other verified functional bugs in the awards transform offline path were found during this audit.

---

# Next Recommended Implementation

## Next Task

### Phase 5 — First investigative SQL scripts

**Phase:** Phase 5

**Why this comes next:**

Ingested + normalized procurement data is ready for forensic questions (vendor totals, concentration, modifications, velocity).

**Dependencies:**

- Populated `vendors` / `awards` / `transactions`
- Prefer running `scripts/run_normalization.py` once against local DB

**Files likely involved:**

- `sql/analysis/vendor_totals.sql`
- `sql/analysis/award_concentration.sql`
- `sql/analysis/modification_analysis.sql`
- `sql/views.sql`

**Definition of Done:**

- [ ] At least vendor totals + modification ratio queries runnable in `psql`
- [ ] Documented in README Phase 5 checklist progress

**Verification command:**

```bash
PGPASSWORD=password psql -h localhost -U argus -d argus -f sql/analysis/vendor_totals.sql
```

---

# Next 5 Tasks

1. Write `sql/analysis/vendor_totals.sql` and related Phase 5 queries
2. Promote reusable joins into `sql/views.sql`
3. Add more pytest coverage for ingestion transforms
4. Implement `bulk_loader.upsert_many`
5. Start Phase 6 rules engine (rapid growth, concentration, etc.)

---

# MVP Progress

## MVP Checklist

- [x] Phase 0 environment ready
- [x] Agency + fiscal year scope chosen (NASA FY2024)
- [x] PostgreSQL schema for vendors/agencies/awards/transactions/risk_flags/risk_scores
- [x] USAspending ingestion works for scope (awards + transactions verified on slice)
- [x] Cleaning/normalization for vendor names and core types
- [ ] SQL analyses: totals, growth, concentration, modifications, velocity
- [ ] Five rules implemented and persisted as flags
- [ ] Simple overall risk score from rules (weights documented)
- [ ] Power BI page(s) for vendor investigation + overview
- [x] Ethics disclaimer visible in README (dashboard tooltip/docs still missing)
- [ ] Sample screenshots saved

```text
MVP Status:                 IN PROGRESS
MVP Completion Estimate:    ~50%
```

---

# Full Project Completion Checklist

Unfinished major capabilities (high level):

- [x] Complete Phase 3 MVP ingestion path (awards + transactions; larger soak optional)
- [x] Phase 4 cleaning/normalization + data-quality report
- [ ] Phase 5 SQL investigation library
- [ ] Phase 6 five forensic rules + `risk_flags`
- [ ] Phase 7 SAM exclusions
- [ ] Phase 8 entity resolution
- [ ] Phases 9–13 stats / features / ML / graph / Argus score
- [ ] Phase 14 DOJ retrospective cases
- [ ] Phase 15 FastAPI
- [ ] Phase 16 Power BI dashboard + screenshots
- [ ] Phase 17 GenAI summaries with guardrails
- [ ] Phase 18 meaningful automated test suite
- [ ] Phase 19 Docker
- [ ] Phase 20 cloud deployment
- [ ] Phase 21 complete documentation set
- [ ] Phase 22 portfolio release gate (secret scan, demos, ethics)

README.md remains the detailed specification. This file records verified reality.

---

# Git Status

```text
Current branch:       main
Recent commit:        652bea6 (prior) — awards path landed earlier
Working tree:         dirty (transaction ingestion + PROGRESS/README updates pending commit)
Uncommitted changes:  src/ingestion/usaspending_transactions.py, scripts/run_ingestion.py, PROGRESS.md, README.md
Remote tracking:      commit after local commit + push
```

Secrets note: `.env` is present locally and ignored by git; `data/raw/**` dumps are ignored; values are not recorded here.

---

# Important Files

```text
README.md
Authoritative roadmap / specification (not runtime truth)

PROGRESS.md
Verified implementation status (this file)

src/config/settings.py
Environment-backed settings loader

src/config/logging.py
Shared logging setup

src/database/connection.py
SQLAlchemy engine/connection helpers

src/database/models.py
ORM models mirroring sql/schema.sql

sql/schema.sql
PostgreSQL DDL source of truth

sql/indexes.sql
Supporting indexes

sql/views.sql
Stub investigator views (not yet real views)

scripts/init_db.sh
Local DB create/apply helper

scripts/run_ingestion.py
CLI entry for USAspending ingestion

src/ingestion/usaspending_client.py
Reusable USAspending HTTP client

src/ingestion/usaspending_awards.py
NASA FY2024 awards ingest pipeline

src/ingestion/usaspending_transactions.py
Transaction ingest scaffold (NotImplemented)

src/ingestion/bulk_loader.py
Batch upsert scaffold (NotImplemented)

docs/data_dictionary.md
Entity/field notes from Phase 1

docs/sources_notes.md
MVP scope + source research log

docs/architecture.md
Architecture / schema decision draft

data/samples/usaspending/*
Tracked tiny API samples + provenance

notebooks/01_data_exploration.ipynb
Phase 1 exploration notebook
```

---

# How to Verify Current State

```bash
cd /home/santiago/Desktop/argus_analytics
source .venv/bin/activate

# Offline checks (always available)
python -m compileall -q src scripts
python -c "from src.config.settings import settings; from src.database.models import Vendor; print(settings.log_level)"
python -c "import json; from pathlib import Path; from src.ingestion.usaspending_awards import transform_award_row; row=json.loads(Path('data/samples/usaspending/sample_awards_response.json').read_text())['results'][0]; print(transform_award_row(row)['award']['award_id'])"
pytest   # currently: no tests collected

# Live checks (require Postgres + network)
pg_isready -h localhost
python -c "from src.database.connection import check_connection; print(check_connection())"
python scripts/run_ingestion.py --awards-only --max-award-pages 1 --award-page-size 5
```

Optional schema re-apply (destructive only if you drop tables first — see comments in `sql/schema.sql`):

```bash
./scripts/init_db.sh
```

---

# Progress Update Rules

Future updates to this file should follow:

1. A task is not complete because a file exists.
2. A task is complete only after functionality is verified.
3. Tests should be run before marking implementation complete.
4. `README.md` describes the target architecture.
5. `PROGRESS.md` describes the actual architecture currently implemented.
6. Blocked work should remain incomplete.
7. Do not claim metrics that have not been measured.
8. Do not claim fraud detection capability from anomaly detection (`HIGH RISK ≠ FRAUD`).
9. Update `Last Reviewed` whenever this file is regenerated.
10. Update this file after each meaningful development milestone.
