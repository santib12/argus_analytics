# Argus — Federal Procurement Risk & Forensic Analytics

> A forensic analytics platform that uses real U.S. government procurement, exclusion, and enforcement data to identify unusual contracting patterns, prioritize entities for investigative review, and explain risk indicators through data-driven analytics.

**Core interpretive rules (non-negotiable):**

```text
HIGH RISK ≠ FRAUD
ANOMALY ≠ MISCONDUCT
```

Argus detects **anomalies**, **unusual procurement patterns**, **compliance indicators**, **risk indicators**, and **relationships that may warrant additional investigative review**. It never claims that an unusual contractor committed fraud.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Current Project Status](#current-project-status)
- [System Architecture](#system-architecture)
- [Public Data Sources](#public-data-sources)
- [Technology Stack](#technology-stack)
- [Final Repository Structure](#final-repository-structure)
- [Data Model](#data-model)
- [Data Ingestion Pipeline](#data-ingestion-pipeline)
- [Entity Resolution](#entity-resolution)
- [Forensic Analytics Engine](#forensic-analytics-engine)
- [Detection Rules](#detection-rules)
- [Statistical Analytics](#statistical-analytics)
- [Machine Learning](#machine-learning)
- [Graph Analytics](#graph-analytics)
- [Risk Scoring](#risk-scoring)
- [DOJ Case Validation](#doj-case-validation)
- [Power BI Dashboard](#power-bi-dashboard)
- [GenAI Investigation Summaries](#genai-investigation-summaries)
- [FastAPI Service](#fastapi-service)
- [Example Investigator Workflow](#example-investigator-workflow)
- [Implementation Roadmap](#implementation-roadmap)
  - [Phase 0 — Repository and Development Environment](#phase-0--repository-and-development-environment)
  - [Phase 1 — Understand the Data](#phase-1--understand-the-data)
  - [Phase 2 — PostgreSQL Database](#phase-2--postgresql-database)
  - [Phase 3 — USAspending Data Ingestion](#phase-3--usaspending-data-ingestion)
  - [Phase 4 — Data Cleaning and Normalization](#phase-4--data-cleaning-and-normalization)
  - [Phase 5 — Core SQL Investigations](#phase-5--core-sql-investigations)
  - [Phase 6 — Rules-Based Forensic Analytics](#phase-6--rules-based-forensic-analytics)
  - [Phase 7 — SAM.gov Exclusion Integration](#phase-7--samgov-exclusion-integration)
  - [Phase 8 — Entity Resolution Implementation](#phase-8--entity-resolution-implementation)
  - [Phase 9 — Statistical Analytics Implementation](#phase-9--statistical-analytics-implementation)
  - [Phase 10 — Feature Engineering](#phase-10--feature-engineering)
  - [Phase 11 — Machine-Learning Anomaly Detection](#phase-11--machine-learning-anomaly-detection)
  - [Phase 12 — Graph Analytics Implementation](#phase-12--graph-analytics-implementation)
  - [Phase 13 — Argus Risk Score](#phase-13--argus-risk-score)
  - [Phase 14 — DOJ Retrospective Case Studies](#phase-14--doj-retrospective-case-studies)
  - [Phase 15 — FastAPI Backend](#phase-15--fastapi-backend)
  - [Phase 16 — Power BI Dashboard](#phase-16--power-bi-dashboard)
  - [Phase 17 — GenAI Investigation Summaries](#phase-17--genai-investigation-summaries-implementation)
  - [Phase 18 — Testing](#phase-18--testing)
  - [Phase 19 — Docker](#phase-19--docker)
  - [Phase 20 — Cloud Deployment](#phase-20--cloud-deployment)
  - [Phase 21 — Documentation](#phase-21--documentation)
  - [Phase 22 — Portfolio Release](#phase-22--portfolio-release)
- [Concepts Learned Through Argus](#concepts-learned-through-argus)
- [Implementation Dependency Map](#implementation-dependency-map)
- [MVP — Minimum Viable Argus](#mvp--minimum-viable-argus)
- [Weekly Development Milestones](#weekly-development-milestones)
- [Development Rules](#development-rules)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Example SQL Analyses](#example-sql-analyses)
- [Testing Strategy](#testing-strategy)
- [Evaluation Metrics](#evaluation-metrics)
- [Ethical and Investigative Limitations](#ethical-and-investigative-limitations)
- [Security and Data Handling](#security-and-data-handling)
- [Potential Resume Bullets](#potential-resume-bullets)
- [Interview Talking Points](#interview-talking-points)
- [Stretch Goals](#stretch-goals)
- [Final Definition of Done](#final-definition-of-done)
- [References](#references)
- [Disclaimer](#disclaimer)

---

# Project Overview

**Argus** is a federal procurement forensic analytics platform built using publicly available U.S. government data.

## What Argus Does

Argus ingests real federal award and transaction records, stores them in a relational database, engineers investigative features, applies rules/statistics/ML/graph analytics, and produces **explainable risk indicators** for investigator review — surfaced through SQL, FastAPI, Power BI, and grounded GenAI summaries.

## What Problem It Addresses

Government procurement systems process enormous volumes of contracting activity across thousands of vendors, agencies, programs, and geographic locations. Manual review cannot efficiently prioritize where to look next.

Potentially interesting patterns may include:

- unusual increases in contract values
- frequent modifications after an initial award
- abnormal vendor concentration within an agency
- repeated clustered awards
- rapid growth in federal obligations
- highly concentrated vendor-agency relationships
- unusual network structures
- entities associated with public exclusion records
- activity resembling patterns observed in known enforcement cases

## Why Federal Procurement Data Is Useful

USAspending.gov publishes real transactional federal spending data with identifiers, agencies, NAICS codes, product/service codes, obligations, and modification history. That makes Argus a **real-data** portfolio project rather than a synthetic fraud toy dataset — while remaining fully reproducible from public sources.

## Why This Is Forensic Analytics (Not Generic ML)

Forensic analytics prioritizes:

1. **Interpretability** — every flag should be explainable
2. **Evidence trails** — provenance and source identifiers are preserved
3. **Investigative workflow** — outputs support human review, not automatic guilt
4. **Multiple evidence layers** — rules, peers, ML, graphs, compliance
5. **Retrospective validation** — compare indicators against known public enforcement cases

Machine learning is one layer — not the product.

## What the System Does Not Claim

The objective is **not** to determine whether an organization committed fraud.

Argus identifies **risk indicators and unusual patterns that may warrant additional review**.

A forensic analytics system should support investigators by prioritizing information and surfacing patterns. It should not automatically make legal conclusions about misconduct.

## Primary Use Case

Argus simulates the workflow of a forensic analytics consultant or investigator reviewing government procurement activity.

A user should be able to search for a federal contractor and receive a structured investigation view containing:

- total federal award volume
- transaction history
- award growth
- agencies awarding the contractor
- product/service categories
- geographic activity
- contract modifications
- exclusion screening results
- anomaly scores
- graph relationships
- triggered forensic rules
- an overall risk score
- a concise investigation summary

Example:

```text
Vendor: ABC Technologies LLC

Argus Risk Score
78 / 100
Elevated

Indicators

HIGH     Rapid award growth
HIGH     Contract modification ratio
MEDIUM   Agency concentration
MEDIUM   Award velocity
NONE     SAM exclusion match

ML Anomaly Score
0.84

Investigation Summary

ABC Technologies experienced a substantial increase in federal
award volume during FY2025 compared with its historical baseline.

Several awards also experienced modification growth materially
above the peer-group median.

No current SAM.gov exclusion match was identified.

These indicators do not establish misconduct and should be
interpreted as signals for additional review.
```

## Project Goals

### Technical Goals

1. ingest large public government datasets
2. normalize inconsistent data
3. design a relational database
4. write complex SQL queries
5. engineer analytical features
6. perform statistical anomaly analysis
7. build machine-learning models
8. perform entity matching across datasets
9. model procurement relationships as graphs
10. expose analytics through an API
11. build an investigator-focused Power BI dashboard
12. use GenAI to explain structured analytical findings

### Investigation Goals

- Which vendors have unusual award patterns?
- Which contracts have unusual modification behavior?
- Which agencies are highly concentrated around specific vendors?
- Which vendors experienced rapid increases in federal award activity?
- Which entities appear in SAM.gov exclusion records?
- Which procurement relationships appear structurally unusual?
- Can historical patterns from known DOJ enforcement cases be detected retrospectively?

## Core Questions Argus Answers

### Vendor Risk

```text
Which vendors have experienced unusually rapid award growth?
```

### Contract Modification Risk

```text
Which contracts increased substantially after their original award?
```

### Concentration Risk

```text
Which vendors receive an unusually large share of an agency's awards?
```

### Transaction Clustering

```text
Are multiple similar awards being issued to the same vendor
within unusually short time periods?
```

### Exclusion Screening

```text
Does a USAspending recipient match an entity appearing in
SAM.gov exclusion records?
```

### Network Risk

```text
Which vendor-agency relationships are unusually concentrated
or structurally important?
```

### Historical Validation

```text
Would Argus have surfaced unusual patterns in a contractor's
public procurement data before a DOJ enforcement action?
```

This project is designed to demonstrate skills relevant to forensic analytics, fraud analytics concepts, AML-style transaction monitoring concepts, regulatory risk, investigations, SQL, ML anomaly detection, graph analytics, data visualization, and GenAI-assisted investigations.

---

# Current Project Status

**Current Phase:** Phase 3 — USAspending Ingestion

**Overall Progress:**

- [x] Phase 0 — Project Setup
- [x] Phase 1 — Data Research
- [x] Phase 2 — PostgreSQL Database
- [ ] Phase 3 — USAspending Ingestion
- [ ] Phase 4 — Data Cleaning
- [ ] Phase 5 — SQL Analytics
- [ ] Phase 6 — Rules Engine
- [ ] Phase 7 — SAM.gov Integration
- [ ] Phase 8 — Entity Resolution
- [ ] Phase 9 — Statistical Analytics
- [ ] Phase 10 — Feature Engineering
- [ ] Phase 11 — Machine Learning
- [ ] Phase 12 — Graph Analytics
- [ ] Phase 13 — Risk Scoring
- [ ] Phase 14 — DOJ Case Studies
- [ ] Phase 15 — FastAPI
- [ ] Phase 16 — Power BI
- [ ] Phase 17 — GenAI Summaries
- [ ] Phase 18 — Testing
- [ ] Phase 19 — Docker
- [ ] Phase 20 — Cloud Deployment
- [ ] Phase 21 — Documentation
- [ ] Phase 22 — Portfolio Release

**How to use this README as a build plan:** open the first unchecked task in the current phase, implement it, mark it complete, and continue until the project is finished.

---

# System Architecture

```text
                         PUBLIC DATA SOURCES

            ┌──────────────────────────────────────┐
            │                                      │
            │ USAspending.gov                     │
            │                                      │
            │ • Awards                            │
            │ • Transactions                      │
            │ • Vendors                           │
            │ • Agencies                          │
            │ • Modifications                     │
            │ • Subawards                         │
            │                                      │
            └───────────────────┬──────────────────┘
                                │
                                ▼
                         Python ETL Layer
                         Pandas / HTTPX / Requests
                                │
                                ▼
                         PostgreSQL Database
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼

          SAM.gov            DOJ Cases       Feature Store
         Exclusions                           / Analytics

              │                 │                 │
              └─────────────────┼─────────────────┘
                                ▼

                       Entity Resolution Layer

                    Exact Match + Fuzzy Match
                 UEI / Name / Address / Aliases

                                │
                                ▼

                    Forensic Analytics Engine

        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼

   Rules Engine          Statistical Models      ML Models

        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼

                         Graph Analytics
                           NetworkX

                                │
                                ▼

                         Risk Scoring Engine

                                │
              ┌─────────────────┴──────────────────┐
              │                                    │
              ▼                                    ▼

          FastAPI API                         Power BI

              │                                    │
              └──────────────────┬─────────────────┘
                                 ▼

                         GenAI Summary Layer

                                 │
                                 ▼

                       Investigator Interface
```

Simplified layer flow:

```text
Public Data
    ↓
Data Ingestion
    ↓
Data Normalization
    ↓
PostgreSQL
    ↓
Feature Engineering
    ↓
Rules / Statistics / ML / Graph Analytics
    ↓
Risk Scoring
    ↓
FastAPI
    ↓
Power BI / Investigation Interface
    ↓
GenAI Investigation Summary
```

## Layer Responsibilities

### Public Data

| Aspect | Detail |
|---|---|
| Responsibility | Provide authoritative, publicly documented source records |
| Input | Government APIs, bulk downloads, published case pages |
| Output | Raw JSON/CSV/HTML extracts saved under `data/raw/` |
| Technologies | USAspending API/bulk, SAM.gov / GSA extracts, DOJ public releases |
| Dependencies | None (external) |

### Data Ingestion

| Aspect | Detail |
|---|---|
| Responsibility | Extract source data reliably with retries, pagination, provenance |
| Input | API endpoints / bulk files / case research notes |
| Output | Raw files + load logs; later transformed rows ready for DB load |
| Technologies | Python, HTTPX/Requests, Pandas |
| Dependencies | Public Data; configuration (`.env`) |

### Data Normalization

| Aspect | Detail |
|---|---|
| Responsibility | Clean types, names, dates, currency; never mutate raw files in place |
| Input | Raw extracts |
| Output | Normalized tables / Parquet / staging frames under `data/processed/` |
| Technologies | Pandas, NumPy, custom normalizers in `src/processing/` |
| Dependencies | Ingestion |

### PostgreSQL

| Aspect | Detail |
|---|---|
| Responsibility | Persist relational entities with keys, constraints, indexes |
| Input | Normalized vendor/agency/award/transaction/exclusion rows |
| Output | Queryable relational warehouse |
| Technologies | PostgreSQL, SQL, SQLAlchemy, psycopg |
| Dependencies | Normalization; schema from Phase 2 |

### Feature Engineering

| Aspect | Detail |
|---|---|
| Responsibility | Convert transactions into vendor-level analytical features |
| Input | SQL aggregates + cleaned tables |
| Output | `vendor_features` rows |
| Technologies | SQL, Pandas, NumPy |
| Dependencies | PostgreSQL populated with cleaned data |

### Rules / Statistics / ML / Graph Analytics

| Aspect | Detail |
|---|---|
| Responsibility | Generate interpretable indicators and anomaly signals |
| Input | Features + relational history |
| Output | `risk_flags`, statistical scores, ML scores, graph metrics |
| Technologies | Python rules, SciPy/NumPy stats, scikit-learn, NetworkX |
| Dependencies | Features; SAM + entity resolution for compliance flags |

### Risk Scoring

| Aspect | Detail |
|---|---|
| Responsibility | Combine evidence into an explainable analytical ranking |
| Input | Component scores (rules, stats, ML, graph, compliance) |
| Output | `risk_scores` with category + explanation |
| Technologies | Python (`src/scoring/`) |
| Dependencies | All analytics layers that contribute components |

### FastAPI

| Aspect | Detail |
|---|---|
| Responsibility | Serve structured investigation results over HTTP |
| Input | PostgreSQL analytical tables |
| Output | JSON responses / OpenAPI docs |
| Technologies | FastAPI, Pydantic, Uvicorn, SQLAlchemy |
| Dependencies | Risk scores and underlying entity tables |

### Power BI / Investigation Interface

| Aspect | Detail |
|---|---|
| Responsibility | Visual investigator workflow (slicers, KPIs, peer views) |
| Input | PostgreSQL views / exported datasets |
| Output | Interactive dashboard + screenshots for portfolio |
| Technologies | Power BI Desktop |
| Dependencies | Populated analytics tables (MVP can start after Phase 6) |

### GenAI Investigation Summary

| Aspect | Detail |
|---|---|
| Responsibility | Convert precomputed JSON findings into readable narrative |
| Input | Structured findings only (never raw unconstrained inventing) |
| Output | Guardrailed investigation summary text |
| Technologies | OpenAI API, prompt templates in `src/genai/` |
| Dependencies | Deterministic analytics must run first |

---

# Public Data Sources

Argus must use **REAL PUBLIC DATA**. Primary sources:

## 1. USAspending.gov

USAspending.gov is the primary transaction and award data source. It provides public information concerning U.S. federal spending.

Channels:

- USAspending.gov UI / research
- USAspending API
- USAspending bulk downloads

Potential fields include:

- award ID
- parent award ID
- federal action obligation
- current award amount
- potential award amount
- recipient name
- recipient UEI
- awarding agency
- funding agency
- award type
- action date
- period of performance
- product or service code
- NAICS code
- place of performance
- award description
- contract modification number
- set-aside type
- recipient location
- transaction history

### Primary Uses

- transaction analysis
- award growth analysis
- contract modification analysis
- agency concentration analysis
- vendor profiling
- geographic analysis
- graph construction
- peer comparison
- anomaly detection

Official site: https://www.usaspending.gov/

API documentation: https://api.usaspending.gov/

## 2. SAM.gov Exclusions

SAM.gov maintains public information about entities excluded from certain forms of federal business. Argus uses this dataset for compliance screening and entity matching (via SAM public extracts and/or GSA public APIs).

Potential fields include:

- entity name
- exclusion type
- exclusion program
- excluding agency
- active date
- termination date
- address
- state
- country
- UEI
- aliases

### Primary Uses

- exact UEI matching
- normalized company-name matching
- fuzzy entity matching
- historical exclusion analysis
- compliance risk indicators

Official information: https://sam.gov/

Open GSA API information: https://open.gsa.gov/

## 3. Department of Justice Enforcement Cases

Public DOJ enforcement announcements provide real cases for **retrospective analysis** (not complete ML fraud labels).

Relevant case types may include:

- procurement fraud
- bid rigging
- price fixing
- market allocation
- false claims
- small-business contracting fraud
- contractor fraud
- corruption-related cases

### Primary Uses

- case studies
- historical validation
- retrospective forensic analysis
- detection-rule evaluation
- documentation

Research question:

> Would Argus have identified unusual publicly visible procurement patterns before the enforcement action?

Official DOJ site: https://www.justice.gov/

Procurement Collusion Strike Force: https://www.justice.gov/atr/procurement-collusion-strike-force

## 4. GSA Public APIs / Extracts

Use publicly documented GSA endpoints and extracts where they support SAM exclusion access, entity identifiers, or related federal entity metadata.

---

# Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Transaction Data | USAspending.gov (API + bulk) |
| Compliance Data | SAM.gov / GSA public APIs & extracts |
| Enforcement Research | DOJ public cases |
| ETL / Analysis | Pandas, NumPy, SciPy |
| HTTP Clients | Requests or HTTPX |
| Database | PostgreSQL |
| ORM / DB access | SQLAlchemy |
| Querying | SQL |
| Machine Learning | scikit-learn (Isolation Forest) |
| Graph Analytics | NetworkX |
| Entity Resolution | RapidFuzz |
| Backend | FastAPI + Pydantic |
| Visualization | Power BI |
| GenAI | OpenAI API |
| Containers | Docker |
| Testing | pytest |
| Version Control | Git / GitHub |
| Cloud (later) | AWS or Azure |

---

# Final Repository Structure

Intended tree (create folders in the phases that own them; do not invent empty complexity early):

```text
argus_analytics/
│
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── data/
│   ├── raw/
│   │   ├── usaspending/
│   │   ├── sam/
│   │   └── doj/
│   ├── processed/
│   │   ├── awards/
│   │   ├── transactions/
│   │   ├── vendors/
│   │   └── exclusions/
│   └── samples/
│
├── sql/
│   ├── schema.sql
│   ├── indexes.sql
│   ├── views.sql
│   └── analysis/
│       ├── vendor_growth.sql
│       ├── award_concentration.sql
│       ├── modification_analysis.sql
│       └── award_clustering.sql
│
├── src/
│   ├── __init__.py
│   ├── config/
│   │   └── settings.py
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   ├── ingestion/
│   │   ├── usaspending_client.py
│   │   ├── usaspending_awards.py
│   │   ├── usaspending_transactions.py
│   │   ├── sam_client.py
│   │   ├── doj_loader.py
│   │   └── bulk_loader.py
│   ├── processing/
│   │   ├── normalize_names.py
│   │   ├── normalize_awards.py
│   │   ├── normalize_entities.py
│   │   ├── validate.py
│   │   └── feature_engineering.py
│   ├── entity_resolution/
│   │   ├── exact_match.py
│   │   ├── fuzzy_match.py
│   │   └── entity_resolver.py
│   ├── analytics/
│   │   ├── rules/
│   │   │   ├── base.py
│   │   │   ├── award_growth.py
│   │   │   ├── modifications.py
│   │   │   ├── concentration.py
│   │   │   ├── clustering.py
│   │   │   └── velocity.py
│   │   ├── statistics/
│   │   │   ├── zscores.py
│   │   │   └── peer_analysis.py
│   │   ├── ml/
│   │   │   ├── anomaly_model.py
│   │   │   └── train.py
│   │   └── graph/
│   │       ├── build_graph.py
│   │       ├── centrality.py
│   │       └── communities.py
│   ├── scoring/
│   │   └── risk_score.py
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   │       ├── vendors.py
│   │       ├── awards.py
│   │       ├── analytics.py
│   │       └── investigations.py
│   └── genai/
│       ├── prompts.py
│       └── investigation_summary.py
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_anomaly_detection.ipynb
│   ├── 04_graph_analysis.ipynb
│   └── 05_doj_case_studies.ipynb
│
├── powerbi/
│   ├── screenshots/
│   └── documentation.md
│
├── tests/
│   ├── conftest.py
│   ├── test_normalization.py
│   ├── test_entity_resolution.py
│   ├── test_rules.py
│   ├── test_features.py
│   ├── test_scoring.py
│   └── test_api.py
│
├── docs/
│   ├── architecture.md
│   ├── methodology.md
│   ├── data_dictionary.md
│   ├── risk_model.md
│   ├── entity_resolution.md
│   ├── ml_methodology.md
│   └── case_studies/
│
└── scripts/
    ├── init_db.sh
    ├── run_ingestion.py
    ├── run_features.py
    └── run_scoring.py
```

## Folder Ownership Guide

### `data/raw/`

- **Belongs:** untouched source downloads/API dumps with provenance metadata
- **Does NOT belong:** cleaned tables, notebooks, credentials
- **Created:** Phase 1–3
- **Owns:** Phase 3 (USAspending), Phase 7 (SAM), Phase 14 (DOJ)

### `data/processed/`

- **Belongs:** normalized intermediate files ready for load or analytics
- **Does NOT belong:** original raw payloads (keep those in `raw/`)
- **Created:** Phase 4
- **Owns:** Phase 4

### `data/samples/`

- **Belongs:** tiny reproducible fixtures for demos/tests
- **Does NOT belong:** full agency fiscal-year dumps
- **Created:** Phase 1 / Phase 18
- **Owns:** Phase 18 primarily

### `sql/`

- **Belongs:** schema, indexes, views, investigative SQL
- **Does NOT belong:** Python business logic
- **Created:** Phase 2 (schema), Phase 5 (analysis)
- **Owns:** Phases 2 and 5

### `src/config/`

- **Belongs:** settings loaded from environment
- **Does NOT belong:** secrets committed in code
- **Created:** Phase 0
- **Owns:** Phase 0

### `src/database/`

- **Belongs:** connection helpers, SQLAlchemy models
- **Does NOT belong:** API route handlers
- **Created:** Phase 2
- **Owns:** Phase 2

### `src/ingestion/`

- **Belongs:** API clients, pagination, loaders
- **Does NOT belong:** risk scoring logic
- **Created:** Phases 3 and 7
- **Owns:** Phases 3 and 7

### `src/processing/`

- **Belongs:** cleaning, validation, feature extraction helpers
- **Does NOT belong:** FastAPI routes
- **Created:** Phases 4 and 10
- **Owns:** Phases 4 and 10

### `src/entity_resolution/`

- **Belongs:** matching hierarchy and confidence logic
- **Does NOT belong:** Power BI files
- **Created:** Phase 8
- **Owns:** Phase 8

### `src/analytics/`

- **Belongs:** rules, stats, ML, graph modules
- **Does NOT belong:** raw data downloads
- **Created:** Phases 6, 9, 11, 12
- **Owns:** those phases

### `src/scoring/`

- **Belongs:** weighted risk combination + explanations
- **Does NOT belong:** model training code (keep in `analytics/ml/`)
- **Created:** Phase 13
- **Owns:** Phase 13

### `src/api/`

- **Belongs:** FastAPI app and routes
- **Does NOT belong:** notebooks
- **Created:** Phase 15
- **Owns:** Phase 15

### `src/genai/`

- **Belongs:** prompts, grounding, summary generation
- **Does NOT belong:** feature math
- **Created:** Phase 17
- **Owns:** Phase 17

### `notebooks/`

- **Belongs:** exploration and narrative analysis only
- **Does NOT belong:** production pipelines (move reusable logic to `src/`)
- **Created:** Phase 1 onward
- **Owns:** exploration across phases; never production

### `powerbi/`

- **Belongs:** PBIX notes, screenshots, dashboard docs
- **Does NOT belong:** database dumps
- **Created:** Phase 16 (MVP may start earlier after Phase 6)
- **Owns:** Phase 16

### `tests/`

- **Belongs:** pytest unit/integration tests and fixtures
- **Does NOT belong:** live secrets
- **Created:** Phase 0 scaffolding; expanded Phase 18
- **Owns:** Phase 18

### `docs/`

- **Belongs:** architecture, methodology, case studies, dictionaries
- **Does NOT belong:** large binary data
- **Created:** Phase 21 (draft earlier as you go)
- **Owns:** Phase 21

### `scripts/`

- **Belongs:** CLI entrypoints to run pipelines
- **Does NOT belong:** core library logic (call into `src/`)
- **Created:** Phase 3 onward
- **Owns:** operational phases

---

# Data Model

The first version should use a relational schema in PostgreSQL.

## `vendors`

```text
vendor_id
recipient_uei
recipient_name
normalized_name
city
state
country
zip_code
created_at
updated_at
```

## `agencies`

```text
agency_id
agency_code
agency_name
subtier_agency_name
```

## `awards`

```text
award_id
vendor_id
awarding_agency_id
funding_agency_id
award_type
description
naics_code
product_service_code
start_date
end_date
initial_value
current_value
potential_value
place_of_performance_state
set_aside_type
```

## `transactions`

```text
transaction_id
award_id
vendor_id
agency_id
action_date
federal_action_obligation
current_total_value
potential_total_value
modification_number
description
created_at
```

## `exclusions`

```text
exclusion_id
uei
entity_name
normalized_name
exclusion_type
excluding_agency
active_date
termination_date
address
city
state
country
```

## `entity_matches`

```text
match_id
vendor_id
exclusion_id
match_type
similarity_score
uei_match
name_match
address_match
review_status
```

## `risk_flags`

```text
risk_flag_id
vendor_id
award_id
flag_type
severity
score
description
detected_at
```

## `vendor_features`

```text
vendor_id
analysis_date
total_award_value
award_count
transaction_count
average_award_value
median_award_value
award_value_std
award_growth_rate
agency_count
agency_concentration
modification_count
average_modification_ratio
award_velocity
geographic_count
set_aside_ratio
graph_degree
graph_weighted_degree
anomaly_score
```

## `risk_scores`

```text
vendor_id
analysis_date
rules_score
statistical_score
ml_score
graph_score
compliance_score
overall_score
risk_level
```

## `doj_cases`

```text
case_id
case_title
defendant_or_entity_name
normalized_name
enforcement_date
agency_or_component
case_url
summary
notes
created_at
```

## Example Schema Snippets

```sql
CREATE TABLE vendors (
    vendor_id           BIGSERIAL PRIMARY KEY,
    recipient_uei       VARCHAR(12),
    recipient_name      TEXT NOT NULL,
    normalized_name     TEXT,
    city                TEXT,
    state               VARCHAR(2),
    country             TEXT,
    zip_code            VARCHAR(20),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE awards (
    award_id                TEXT PRIMARY KEY,
    vendor_id               BIGINT NOT NULL REFERENCES vendors(vendor_id),
    awarding_agency_id      BIGINT REFERENCES agencies(agency_id),
    funding_agency_id       BIGINT REFERENCES agencies(agency_id),
    award_type              TEXT,
    description             TEXT,
    naics_code              VARCHAR(10),
    product_service_code    VARCHAR(10),
    start_date              DATE,
    end_date                DATE,
    initial_value           NUMERIC(20, 2),
    current_value           NUMERIC(20, 2),
    potential_value         NUMERIC(20, 2),
    place_of_performance_state VARCHAR(2),
    set_aside_type          TEXT
);

CREATE INDEX idx_transactions_vendor ON transactions(vendor_id);
CREATE INDEX idx_transactions_action_date ON transactions(action_date);
CREATE INDEX idx_awards_agency ON awards(awarding_agency_id);
CREATE INDEX idx_vendors_uei ON vendors(recipient_uei);
CREATE INDEX idx_exclusions_uei ON exclusions(uei);
```

---

# Data Ingestion Pipeline

ETL means **Extract → Transform → Load**.

## Step 1 — Extract

Retrieve data through:

- USAspending API
- USAspending bulk downloads
- SAM.gov API or extracts
- structured DOJ case research

Example conceptual Python flow:

```python
def fetch_transactions(filters):
    response = requests.post(
        USASPENDING_ENDPOINT,
        json=filters,
        timeout=60
    )

    response.raise_for_status()
    return response.json()
```

Always save raw responses under `data/raw/` before transforming.

## Step 2 — Normalize

Government datasets often contain:

- inconsistent capitalization
- abbreviations
- punctuation differences
- missing values
- duplicate entities
- inconsistent addresses

Example normalization:

```text
ACME TECHNOLOGIES, L.L.C.
ACME Technologies LLC
Acme Technologies, LLC

↓

ACME TECHNOLOGIES LLC
```

## Step 3 — Load

Load normalized data into PostgreSQL. Use batch inserts rather than individual inserts for performance. Preserve source identifiers.

## Step 4 — Index

Indexes should be added to commonly queried fields (see Data Model). Never modify raw source files in place.

---

# Entity Resolution

Entity resolution connects records that refer to the same real-world organization.

This is particularly important when matching USAspending recipients against SAM.gov exclusions.

## Matching Hierarchy

### Level 1 — Exact UEI Match

Highest confidence.

```text
USAspending UEI == SAM.gov UEI
```

### Level 2 — Exact Normalized Name

```text
ACME TECHNOLOGIES, LLC
↓
ACME TECHNOLOGIES LLC
```

### Level 3 — Fuzzy Name Match

Use RapidFuzz.

```python
from rapidfuzz import fuzz

score = fuzz.token_sort_ratio(
    vendor_name,
    exclusion_name
)
```

### Level 4 — Name + Geographic Match

Combine company-name similarity with state, city, and address.

## Example Match Score

```text
Name similarity      95
State match          Yes
City match           Yes
UEI match            No

Composite confidence
92 / 100
```

Low-confidence fuzzy matches should require manual review. Always store confidence and match method.

---

# Forensic Analytics Engine

The analytics engine layers evidence:

```text
Rules Engine
Statistical Analytics
Machine Learning
Graph Analytics
```

Each layer produces individual indicators. Those indicators are then combined into an overall risk score.

Important vocabulary:

| Term | Meaning in Argus |
|---|---|
| Rule | Deterministic check with documented parameters |
| Indicator | A measured signal that something is unusual |
| Alert / Flag | Persisted result of a triggered rule/indicator |
| Evidence | Supporting metrics and source records behind a flag |
| Fraud determination | **Out of scope** — never produced by Argus |

---

# Detection Rules

Implement interpretable rules **before** advanced ML.

For every rule, document: purpose, mathematical definition, parameters, input columns, output, possible legitimate explanations, and limitations.

## Rule 1 — Rapid Award Growth

**Purpose:** Detect vendors whose federal award volume rose sharply versus their own baseline and peers.

**Question:** Has a vendor's federal award volume increased significantly relative to its historical baseline?

Example:

```text
FY2023     $1.4M
FY2024     $1.8M
FY2025     $3.2M
FY2026     $14.9M
```

**Definition:**

```text
growth_rate = (current_period - previous_period) / previous_period
```

**Parameters:** lookback years, minimum prior obligations, peer percentile threshold.

**Inputs:** vendor_id, fiscal-year obligation sums.

**Output:** risk flag `rapid_award_growth` with severity and growth_rate.

**Legitimate explanations:** emergency contracting, legitimate expansion, policy shifts, disaster response.

**Limitations:** new vendors lack baseline; fiscal-year boundaries can distort growth.

## Rule 2 — Unusual Contract Modification Ratio

**Purpose:** Flag awards whose current value is much larger than initial value.

Example:

```text
Original Award   $900,000
Final Value      $3,150,000
Increase         3.5x
```

**Definition:**

```text
modification_ratio = current_award_value / initial_award_value
```

Prefer peer-based thresholds rather than arbitrary universal thresholds.

**Legitimate explanations:** scope changes, multi-year options exercised, legitimate contract evolution.

**Limitations:** missing initial values; award type differences.

## Rule 3 — Agency Concentration

**Purpose:** Measure vendor dependence on a single awarding agency.

Example:

```text
Vendor ABC
Agency A        82%
Agency B        11%
Agency C         7%
```

**Definitions:**

```text
largest_agency_share = largest_agency_award_value / total_vendor_award_value
HHI = Σ(s_i²)
```

**Legitimate explanations:** specialized suppliers, sole-source niches, agency-specific capabilities.

**Limitations:** small vendors naturally concentrate; HHI sensitive to sparse data.

## Rule 4 — Clustered Awards

Identify sequences of similar awards occurring within short windows (vendor, agency, value, PSC, dates).

Example:

```text
Aug 10     $48,500
Aug 11     $49,200
Aug 11     $47,800
Aug 12     $49,600
Aug 13     $48,100
```

Describe results as:

```text
Clustered award activity detected
```

not:

```text
Contract splitting confirmed
```

**Legitimate explanations:** task-order patterns, recurring service needs, legitimate packaging.

**Limitations:** window/size parameters are judgment calls; correlation ≠ scheme.

## Rule 5 — Award Velocity

Measure how rapidly a vendor receives new federal obligations.

```text
Historical baseline: 4 transactions/month
Recent period:      29 transactions/month

velocity_ratio = recent_transaction_rate / historical_transaction_rate
```

**Legitimate explanations:** surge requirements, new capability awards, seasonal cycles.

**Limitations:** short histories produce unstable rates.

## Rule 6 — Unusual Modification Frequency

```text
modifications_per_award
```

Compare against vendor history, industry peers, same agency, same NAICS, same PSC.

**Legitimate explanations:** complex systems contracts, evolving requirements.

**Limitations:** modification numbering conventions vary.

## Rule 7 — Exclusion Match

If a vendor matches an active exclusion record:

```text
Compliance Flag
SAM_EXCLUSION_MATCH
```

Treat as a high-priority **compliance indicator**. Preserve match method, confidence, exclusion status, and source information.

**Legitimate explanations:** name collision / false-positive fuzzy match — always review confidence.

**Limitations:** entity resolution errors; historical vs active status confusion.

---

# Statistical Analytics

Compare vendors against appropriate peer groups:

- NAICS industry
- product/service code
- agency
- award type
- fiscal year

## Z-Scores

```text
Vendor modification ratio   4.1
Peer mean                   1.3
Peer standard deviation     0.7
Z-score                     4.0
```

A high absolute z-score indicates unusual behavior relative to the peer population.

## Percentile Ranking

```text
Award growth             98th percentile
Modification ratio       99th percentile
Agency concentration     93rd percentile
```

## Robust Statistics

Procurement datasets may contain extreme outliers. Median and Median Absolute Deviation (MAD) can be more appropriate than means in some analyses. Also use IQR/quartiles for outlier fences.

---

# Machine Learning

The first ML model should be **unsupervised anomaly detection**.

This avoids pretending that all public procurement transactions have reliable fraud labels.

## Recommended Model — Isolation Forest

```python
from sklearn.ensemble import IsolationForest

model = IsolationForest(
    n_estimators=300,
    contamination="auto",
    random_state=42
)

model.fit(X)
scores = model.decision_function(X)
predictions = model.predict(X)
```

Possible features:

```text
total_award_value
award_count
transaction_count
average_award_value
median_award_value
award_value_std
award_growth_rate
agency_count
agency_concentration
modification_count
modification_ratio
award_velocity
geographic_dispersion
set_aside_ratio
graph_degree
graph_weighted_degree
```

## Why Unsupervised Learning?

There is no comprehensive public dataset labeling every contractor as fraud / not fraud.

**Do NOT optimize a model using DOJ cases as if they represented complete ground truth.**

Treating DOJ enforcement actions as complete fraud labels introduces **selection bias**: known cases are only misconduct that was detected, investigated, and publicly announced — not a representative sample.

Pipeline:

```text
Isolation Forest
        ↓
Unusual vendor behavior
        ↓
Risk indicator
        ↓
Human review
```

---

# Graph Analytics

Procurement relationships can be represented as a graph.

## Initial Bipartite Network

- Node type 1: Vendor
- Node type 2: Agency
- Edges: federal award relationships
- Edge weights: total obligated value

```text
             Vendor A
            /   |    \
           /    |     \
        Army   Navy   DLA
```

Later graphs may include Vendor ↔ Award and Prime ↔ Subaward.

## Graph Metrics

- **Degree / Degree Centrality:** how many agencies connect to a vendor?
- **Weighted Degree:** how much obligation value flows through those relationships?
- **Betweenness Centrality:** structurally important positions
- **Community Detection:** clusters of vendors/agencies/categories
- **Concentration:** unusually dominant vendor-agency ties

---

# Risk Scoring

Argus produces an **analytical ranking**, not a probability of fraud.

Example conceptual model:

```text
Rules Score           30%
Statistical Score     20%
ML Score              20%
Graph Score           15%
Compliance Score      15%
```

Example:

```text
Rules                 82
Statistics            74
ML                    91
Graph                 63
Compliance             0
Overall               71
```

Suggested risk levels (project-defined analytical categories only):

```text
0–29     Low
30–49    Moderate
50–69    Elevated
70–84    High
85–100   Critical Review
```

Every score must be explainable. No score implies criminal guilt.

---

# DOJ Case Validation

Retrospective validation workflow:

```text
DOJ case
↓
identify vendor
↓
determine enforcement date
↓
collect historical procurement data before enforcement
↓
run Argus
↓
measure anomaly indicators
```

### Methodology Steps

1. Identify a publicly documented DOJ procurement case.
2. Identify organizations appearing in the case.
3. Retrieve their historical USAspending activity.
4. Define a cutoff date before the enforcement announcement.
5. Run Argus using only information available before enforcement.
6. Measure which indicators were triggered.

Example research question:

```text
Would Argus have ranked the entity as unusual
before the DOJ enforcement action became public?
```

**Important:** Argus surfacing an entity ≠ Argus predicting fraud. A successful retrospective result demonstrates that certain public procurement patterns were analytically unusual — not that the system predicted misconduct.

---

# Power BI Dashboard

Design for an investigator, not vanity charts.

## Page 1 — Executive Risk Overview

KPIs (example placeholders — replace with measured values):

```text
Total Awards Analyzed
Transactions
Vendors
Elevated-Risk Vendors
```

Charts: risk distribution, awards over time, top agencies, top industries, vendors by risk percentile, geographic award map.

## Page 2 — Vendor Investigation

Search vendor → show Argus Risk Score, ML Anomaly Score, and indicator table.

## Page 3 — Award History

Obligations over time, transactions, modifications, original vs current value, agency breakdown.

## Page 4 — Peer Analysis

Compare selected vendor vs same NAICS / PSC / agency peers.

## Page 5 — Network Analysis

Vendor ↔ agency award relationships visualization.

## Page 6 — Exclusion Screening

Match status, confidence, method.

## Page 7 — Investigation Summary

Concise narrative from structured analytics (later GenAI-assisted).

---

# GenAI Investigation Summaries

**Argus must calculate findings BEFORE calling the LLM.**

```text
Analytics Engine
↓
JSON findings
↓
LLM
↓
Human-readable summary
```

Example structured input:

```json
{
  "vendor": "ABC Technologies LLC",
  "risk_score": 78,
  "anomaly_score": 0.84,
  "flags": [
    {"type": "rapid_award_growth", "severity": "high"},
    {"type": "high_modification_ratio", "severity": "high"},
    {"type": "agency_concentration", "severity": "medium"}
  ],
  "sam_exclusion_match": false
}
```

## GenAI Guardrails

```text
You are generating an analytical investigation summary.

Only describe facts contained in the structured input.

Do not accuse an entity of fraud, corruption, misconduct,
collusion, or criminal activity.

Describe findings as indicators, anomalies, or patterns
that may warrant further review.
```

Concepts: LLM, prompt, hallucination, grounding, structured input, guardrails.

---

# FastAPI Service

Example endpoints:

```text
GET  /health
GET  /vendors
GET  /vendors/{id}
GET  /vendors/{id}/risk
GET  /vendors/{id}/transactions
GET  /vendors/{id}/network
GET  /vendors/{id}/exclusions
GET  /analytics/high-risk-vendors
POST /investigations/{id}/summary
```

Example response:

```json
{
  "vendor_id": 1289,
  "vendor_name": "ABC Technologies LLC",
  "risk_score": 78,
  "risk_level": "High",
  "anomaly_score": 0.84,
  "flags": [
    "rapid_award_growth",
    "high_modification_ratio",
    "agency_concentration"
  ]
}
```

---

# Example Investigator Workflow

An investigator enters `ABC Technologies LLC`. Argus performs:

```text
1. Locate vendor
2. Retrieve award history
3. Retrieve transaction history
4. Calculate vendor features
5. Compare vendor against peers
6. Run detection rules
7. Run anomaly model
8. Analyze graph relationships
9. Screen SAM.gov exclusions
10. Calculate risk score
11. Build investigation summary
```

Output disposition language must remain analytical:

```text
Recommended Disposition
-----------------------
Prioritize for additional analytical review
```

Not: "guilty", "fraud confirmed", or equivalent.

---

# Implementation Roadmap

Do not try to build the entire platform at once. Complete phases in order unless the dependency map explicitly says work can run in parallel. After each phase, mark the matching checkbox under [Current Project Status](#current-project-status).

---

# Phase 0 — Repository and Development Environment

### Objective

Create a reproducible local development environment with Git, Python virtualenv, configuration management, logging, and the initial directory scaffold — with **zero secrets in Git**.

### Concepts to Learn

- **Python virtual environments:** isolate project dependencies from system Python
- **Dependency management:** pin packages via `requirements.txt` / `pyproject.toml` so others get the same stack
- **Environment variables:** runtime configuration outside source code
- **Git repositories:** version history, branches, commits
- **`.gitignore`:** prevent committing secrets, caches, raw dumps, virtualenvs
- **Separation of configuration and secrets:** `.env.example` is a template; `.env` holds real secrets locally only
- **Reproducible development environments:** another developer can follow README and reach the same starting point
- **Logging:** structured observability for ETL and API later

**Why secrets must never be committed:** API keys, database passwords, and cloud credentials in Git history can be scraped, reused for abuse, and are hard to fully erase even after deletion. Argus uses public data, but still needs private credentials for SAM (if required), OpenAI, and database access.

### Files to Create

```text
README.md                  (this document — already being established)
LICENSE
.gitignore
.env.example
requirements.txt
pyproject.toml             (optional early; recommended by Phase 18)
src/__init__.py
src/config/__init__.py
src/config/settings.py
src/config/logging.py
scripts/.gitkeep
data/raw/.gitkeep
data/processed/.gitkeep
data/samples/.gitkeep
tests/__init__.py
docs/.gitkeep
```

### Implementation Checklist

- [x] **Initialize Git repository**
  - File: repository root
  - Depends on: none
  - Concepts: Git, version control
  - Output: `.git/` present
  - Test: `git status` works
- [x] Confirm remote strategy (GitHub) without pushing secrets later
  - Remote: `origin` → `https://github.com/santib12/argus_analytics.git`
  - Secrets stay in ignored `.env` only; never commit or push credentials
- [x] **Create / maintain README.md** as the technical spec + checklist
- [x] **Create `.gitignore`**
  - File: `.gitignore`
  - Include at minimum: `.env`, `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`, IDE folders, `data/raw/**` (except `.gitkeep`), large dumps, Power BI temp files, model binaries if desired
- [x] **Create `.env.example`**
  - File: `.env.example`
  - Keys: `DATABASE_URL`, `USASPENDING_BASE_URL`, `SAM_API_KEY`, `OPENAI_API_KEY`, `LOG_LEVEL`
- [x] Create Python virtual environment: `python -m venv .venv`
- [x] Activate venv (`source .venv/bin/activate` on Linux/macOS)
- [x] Create project directory structure (`src/`, `sql/`, `data/`, `tests/`, `docs/`, `scripts/`, `notebooks/`, `powerbi/`)
- [x] Create `requirements.txt` with initial packages (pandas, numpy, scipy, scikit-learn, networkx, rapidfuzz, requests, httpx, fastapi, uvicorn, sqlalchemy, psycopg2-binary, python-dotenv, pydantic, openai, jupyter, matplotlib, pytest)
- [x] Optionally create `pyproject.toml` for package metadata / pytest config
- [x] Install development dependencies: `pip install -r requirements.txt`
- [x] Copy `.env.example` → `.env` and configure local placeholders
- [x] **Add configuration module**
  - File: `src/config/settings.py`
  - Depends on: python-dotenv, `.env`
  - Concepts: configuration vs secrets
  - Output: typed settings object / getters
  - Test: load `DATABASE_URL` without hardcoding
- [x] **Add basic logging**
  - File: `src/config/logging.py`
  - Output: consistent logger factory
  - Test: emit INFO log from a tiny script
- [x] Add `LICENSE` (choose an open-source license appropriate for your portfolio)
- [x] Verify `git check-ignore -v .env` shows `.env` is ignored
- [x] Create initial Git commit (no secrets)

### Definition of Done

A clean clone (plus local `.env`) can create a venv, install requirements, import `src.config.settings`, and log a message. No credentials exist in the repository.

### Testing

- [x] `python -c "from src.config.settings import settings; print(settings)"` (or equivalent)
- [x] Confirm `.env` is untracked
- [x] Confirm directory scaffold exists

### Common Mistakes

- Committing `.env` or real API keys
- Installing packages globally instead of in `.venv`
- Putting production logic only in notebooks
- Ignoring large raw data files until the repo becomes huge
- Writing Windows-only activate instructions without Linux/macOS paths

---

# Phase 1 — Understand the Data

### Objective

Learn USAspending, SAM.gov exclusions, and DOJ case sources deeply enough to design schema and ingestion correctly. Select a **small initial development dataset**.

**Recommended starting scope:**

```text
ONE federal agency
+
ONE fiscal year
```

**Why:** full-federal multi-year data is huge, slow, expensive to iterate on, and hides ETL bugs under volume. Start small, prove the pipeline, then expand.

### Concepts to Learn

- **API / REST API:** programmatic HTTP interfaces returning structured data
- **JSON:** common response format for USAspending
- **Pagination:** retrieving large result sets page by page
- **HTTP GET / HTTP POST:** USAspending often uses POST for search endpoints
- **Rate limits / timeouts / retries:** polite, resilient clients
- **Public datasets & data dictionaries:** field definitions and caveats
- **Identifiers:** award IDs, transaction IDs
- **UEI:** Unique Entity Identifier for entities
- **NAICS:** industry classification
- **Product Service Codes (PSC):** what was bought
- **Federal obligations / awards / award modifications / fiscal years**

### Files to Create

```text
docs/data_dictionary.md          (draft)
docs/sources_notes.md
data/samples/usaspending/        (small sample JSON/CSV)
notebooks/01_data_exploration.ipynb
```

### Implementation Checklist

- [x] **Read USAspending API documentation**
  - File: notes in `docs/sources_notes.md`
  - Depends on: Phase 0
  - Concepts: REST, JSON
  - Output: list of relevant endpoints
  - Test: open docs URL and capture endpoint names
- [x] Identify relevant endpoints (awards search, transactions, recipient profiles, etc.)
- [x] Identify bulk download options and file layouts
- [x] Download sample award data (small)
- [x] Download sample transaction data (small)
- [x] Inspect JSON response structure
- [x] Identify primary keys
- [x] Identify important foreign-key relationships (award ↔ transaction ↔ recipient ↔ agency)
- [x] Identify null-heavy fields
- [x] Identify vendor identifiers (UEI, name, location)
- [x] Identify agency identifiers (toptier/subtier codes/names)
- [x] Document data dictionary draft in `docs/data_dictionary.md`
- [x] Examine SAM exclusion structure (fields, active vs terminated)
- [x] Identify SAM identifiers (UEI, names, aliases)
- [x] Identify DOJ case sources (press releases, PCSF materials)
- [x] Select initial development dataset (agency + fiscal year) and write it down in `docs/sources_notes.md`
- [x] Save samples under `data/samples/` for tests (not full dumps)
- [x] Record provenance: download date, endpoint/URL, filters used

### Definition of Done

You can explain the key entities/keys for USAspending awards and transactions, have sample files saved, and have a documented agency+FY scope for MVP ingestion.

### Testing

- [x] Open sample JSON and list top-level keys
- [x] Manually join one award to its transactions conceptually
- [x] Confirm sample files are small enough for Git or kept local intentionally

### Common Mistakes

- Downloading all federal years on day one
- Assuming UEI is always present and clean
- Treating display names as stable primary keys
- Skipping the data dictionary and inventing column meanings later
- Mixing award-level and transaction-level grains in one table without care

---

# Phase 2 — PostgreSQL Database

### Objective

Install PostgreSQL, create the `argus` database, and implement a relational schema with keys, constraints, and indexes for vendors, agencies, awards, transactions, exclusions, matches, features, flags, scores, and DOJ cases.

### Concepts to Learn

- Relational databases, tables, primary keys, foreign keys
- Normalization (reduce redundant inconsistent copies)
- Indexes (speed selective filters/joins)
- Joins, constraints, transactions
- Schema design for analytical workloads

### Files to Create

```text
sql/schema.sql
sql/indexes.sql
sql/views.sql                 (stub ok)
src/database/connection.py
src/database/models.py        (SQLAlchemy models; can start after raw SQL)
scripts/init_db.sh
```

### Implementation Checklist

- [x] Install PostgreSQL locally
- [x] Create `argus` database
- [x] Create database user with least-privilege local access
- [x] Configure `DATABASE_URL` in `.env`
- [x] **Write `sql/schema.sql`**
  - File: `sql/schema.sql`
  - Depends on: Phase 1 data dictionary
  - Concepts: PKs, FKs, types
  - Output: executable schema
  - Test: `psql -d argus -f sql/schema.sql`
- [x] Create `vendors` table
- [x] Create `agencies` table
- [x] Create `awards` table
- [x] Create `transactions` table
- [x] Create `exclusions` table
- [x] Create `entity_matches` table
- [x] Create `vendor_features` table
- [x] Create `risk_flags` table
- [x] Create `risk_scores` table
- [x] Create `doj_cases` table
- [x] Add foreign keys
- [x] Add unique constraints (e.g., natural award IDs, UEI where appropriate)
- [x] Add indexes in `sql/indexes.sql`
- [x] **Create DB connection module**
  - File: `src/database/connection.py`
  - Depends on: settings
  - Output: engine/session helpers
  - Test: successful `SELECT 1`
- [x] Test inserts (manual sample rows)
- [x] Test joins (vendor ↔ awards ↔ transactions)
- [x] Document schema decisions in `docs/architecture.md` draft

### Definition of Done

Schema applies cleanly on a fresh database; sample inserts and joins succeed; Python can connect via `DATABASE_URL`.

### Testing

```sql
INSERT INTO vendors (recipient_name, normalized_name) VALUES ('TEST VENDOR LLC', 'TEST VENDOR LLC');
SELECT * FROM vendors;
```

- [x] Re-run schema on empty DB without errors
- [x] Confirm FK rejects orphan award rows

### Common Mistakes

- Using vendor name as the only primary key
- No indexes on join/filter columns
- Mixing stringly-typed dates/currency
- Creating tables ad hoc from Pandas without constraints
- Storing mutable derived scores without `analysis_date`

---

# Phase 3 — USAspending Data Ingestion

### Objective

Build a resilient ETL path that extracts USAspending awards/transactions for the chosen agency+FY, saves raw payloads, transforms them, and loads vendors/agencies/awards/transactions into PostgreSQL without duplicates.

### Concepts to Learn

- API clients, pagination, retries, timeouts
- HTTP status codes
- Batch processing
- ETL (Extract, Transform, Load)
- Idempotent loads / upserts
- Provenance logging

### Files to Create

```text
src/ingestion/usaspending_client.py
src/ingestion/usaspending_awards.py
src/ingestion/usaspending_transactions.py
src/ingestion/bulk_loader.py
scripts/run_ingestion.py
data/raw/usaspending/
```

### Implementation Checklist

- [ ] **Create reusable API client**
  - File: `src/ingestion/usaspending_client.py`
  - Depends on: configuration module
  - Concepts: REST APIs, HTTP, pagination
  - Output: reusable API client
  - Test: successfully retrieve and parse one API response
- [ ] Configure base URL from settings (`USASPENDING_BASE_URL`)
- [ ] Add HTTP timeout
- [ ] Add retries with backoff for transient failures
- [ ] Implement pagination
- [ ] Validate HTTP responses (`raise_for_status`, schema sanity checks)
- [ ] Fetch awards for selected agency + fiscal year
- [ ] Fetch transactions for selected scope
- [ ] Save raw API responses under `data/raw/usaspending/`
- [ ] Transform raw responses into tabular records
- [ ] Load vendors (dedupe by UEI/normalized name strategy)
- [ ] Load agencies
- [ ] Load awards
- [ ] Load transactions
- [ ] Prevent duplicate records (upsert / unique constraints)
- [ ] Add logging (counts, failures, durations)
- [ ] Add ingestion statistics summary (records attempted/inserted/skipped)
- [ ] Test ingestion on small dataset
- [ ] Test ingestion on larger dataset within same agency/FY
- [ ] Create CLI entrypoint `scripts/run_ingestion.py`

### Definition of Done

Running the ingestion script populates vendors, agencies, awards, and transactions for the chosen scope; re-running does not create uncontrolled duplicates; raw files exist for audit.

### Testing

- [ ] Count rows in each core table
- [ ] Spot-check one vendor’s awards against USAspending UI
- [ ] Simulate API timeout and confirm retry behavior
- [ ] Confirm raw files are not overwritten silently without versioning/provenance

### Common Mistakes

- Transforming without saving raw responses
- Ignoring pagination and thinking the first page is complete
- Inserting row-by-row in a Python loop without batches
- No unique keys → duplicate storms on re-runs
- Expanding to all agencies before the client is stable

---

# Phase 4 — Data Cleaning and Normalization

### Objective

Create reusable cleaning functions for company names, addresses, UEIs, dates, currency, and agency names; produce normalized fields and a data-quality report without altering raw source files.

### Concepts to Learn

- Dirty data realities in government datasets
- Normalization of strings/types
- Missing values, duplicates
- Company-name normalization (LLC variants)
- Type conversion and date/currency normalization
- Categorical value hygiene

### Files to Create

```text
src/processing/normalize_names.py
src/processing/normalize_awards.py
src/processing/normalize_entities.py
src/processing/validate.py
tests/test_normalization.py
data/processed/
docs/data_quality_report.md   (generated or templated)
```

### Implementation Checklist

- [ ] **Create company-name normalization function**
  - File: `src/processing/normalize_names.py`
  - Depends on: Phase 3 data available
  - Concepts: string normalization
  - Output: `normalize_company_name()`
  - Test: `"ACME TECHNOLOGIES, L.L.C." → "ACME TECHNOLOGIES LLC"`
- [ ] Normalize capitalization
- [ ] Remove unnecessary punctuation from company names
- [ ] Normalize LLC / L.L.C. / Inc. variants
- [ ] Normalize whitespace
- [ ] Normalize dates to ISO / DATE types
- [ ] Normalize currency values to numeric
- [ ] Handle null values explicitly (do not silently invent)
- [ ] Detect duplicates
- [ ] Validate UEIs (length/charset rules as documented)
- [ ] Create normalized vendor names in DB (`normalized_name`)
- [ ] Normalize addresses / state codes where feasible
- [ ] Normalize agency names/codes mapping
- [ ] Log rejected rows with reasons
- [ ] Generate data-quality report (null rates, dupes, reject counts)
- [ ] Write cleaned outputs to `data/processed/` and/or update DB staging fields
- [ ] Add unit tests for normalizers

### Definition of Done

Normalization functions are tested; vendors have `normalized_name`; a written data-quality report exists; raw files remain untouched.

### Testing

```python
assert normalize_company_name("ACME TECHNOLOGIES, L.L.C.") == "ACME TECHNOLOGIES LLC"
```

- [ ] Run validation over ingested tables and save metrics
- [ ] Confirm rejected-row log exists

### Common Mistakes

- Over-normalizing and collapsing distinct entities
- Editing files in `data/raw/`
- Dropping null UEI rows without logging
- Locale-dependent date parsing
- Assuming punctuation removal is always safe for all legal names

---

# Phase 5 — Core SQL Investigations

### Objective

Write investigative SQL that answers core forensic questions using GROUP BY, HAVING, CTEs, window functions, joins, and temporal analysis. Store queries under `sql/analysis/`.

### Concepts to Learn

- GROUP BY / HAVING
- CTEs
- Window functions
- Aggregations
- Temporal analysis
- Peer comparisons via SQL

### Files to Create

```text
sql/analysis/vendor_totals.sql
sql/analysis/vendor_growth.sql
sql/analysis/award_concentration.sql
sql/analysis/modification_analysis.sql
sql/analysis/award_velocity.sql
sql/analysis/peer_groups.sql
sql/views.sql
```

### Implementation Checklist

- [ ] Total obligations by vendor
- [ ] Award count by vendor
- [ ] Transactions by vendor
- [ ] Vendor activity by fiscal year
- [ ] Vendor growth year-over-year
- [ ] Award modifications
- [ ] Modification ratios
- [ ] Awards by agency
- [ ] Vendor dependency on agencies
- [ ] Award velocity
- [ ] NAICS peer groups
- [ ] Product Service Code peer groups
- [ ] Top vendors by obligation value
- [ ] Create helpful views for Power BI later
- [ ] Document each query purpose in comments at file top

**Detailed example task:**

- [ ] **Write vendor growth YoY query**
  - File: `sql/analysis/vendor_growth.sql`
  - Depends on: populated transactions
  - Concepts: CTEs, window functions
  - Output: vendor/year/obligations/growth_rate
  - Test: returns rows for sample vendor with known yearly sums

### Definition of Done

All listed analyses run successfully against real ingested data and produce sensible investigator-facing result sets.

### Testing

- [ ] Compare SQL totals for one vendor against a manual Pandas check
- [ ] Explain one surprising result (data issue vs true pattern)

### Common Mistakes

- Mixing award grain and transaction grain incorrectly
- Double-counting modifications
- Using SELECT * in final analytical artifacts
- No filters for scope (agency/FY) while interpreting “top vendors”
- Forgetting fiscal-year vs calendar-year definitions

---

# Phase 6 — Rules-Based Forensic Analytics

### Objective

Implement a rules engine with a shared result model and at least five core forensic rules, persist `risk_flags`, and document each rule’s methodology. This is the analytical heart of the **MVP**.

### Concepts to Learn

- Rule vs indicator vs alert vs evidence vs fraud determination
- Parameterized thresholds
- Severity levels
- Explainability
- Persisting analytical outputs with timestamps

### Files to Create

```text
src/analytics/rules/base.py
src/analytics/rules/award_growth.py
src/analytics/rules/modifications.py
src/analytics/rules/concentration.py
src/analytics/rules/clustering.py
src/analytics/rules/velocity.py
src/analytics/rules/exclusion.py          (stub until Phase 7–8)
docs/methodology.md                       (rule section)
tests/test_rules.py
scripts/run_rules.py
```

### Implementation Checklist

- [ ] **Create rule interface**
  - File: `src/analytics/rules/base.py`
  - Depends on: DB access, features or SQL extracts
  - Concepts: interface / polymorphism
  - Output: common `Rule` protocol + runner
  - Test: dummy rule returns structured result
- [ ] Create common rule result model (vendor_id, flag_type, severity, score, description, evidence JSON)
- [ ] Document every rule (purpose, math, params, inputs, outputs, legitimate explanations, limitations)
- [ ] Implement rapid award growth
- [ ] Test rapid award growth
- [ ] Implement modification ratio
- [ ] Test modification ratio
- [ ] Implement agency concentration
- [ ] Test agency concentration
- [ ] Implement clustered awards
- [ ] Test clustered awards
- [ ] Implement award velocity
- [ ] Test award velocity
- [ ] Implement modification frequency (optional stretch within phase)
- [ ] Persist generated risk flags to `risk_flags`
- [ ] Add rule severity levels (LOW/MEDIUM/HIGH)
- [ ] Ensure output language never asserts fraud
- [ ] Create `scripts/run_rules.py`

### Definition of Done

Five rules execute on real data, write flags to PostgreSQL, have unit tests, and have methodology documentation with legitimate alternate explanations.

### Testing

- [ ] Fixture vendor that should trigger growth rule
- [ ] Fixture vendor that should not
- [ ] Verify flags are explainable from stored evidence fields

### Common Mistakes

- Hard-coding universal thresholds with no peer context
- Naming flags “fraud_detected”
- No tests for boundary conditions (zero baseline)
- Running rules before SQL sanity checks
- Losing parameter versions (cannot reproduce why a flag fired)

---

# Phase 7 — SAM.gov Exclusion Integration

### Objective

Ingest public SAM exclusion records into PostgreSQL with active/termination dates, agency, UEI when available, and normalized names — ready for matching in Phase 8.

### Concepts to Learn

- Sanctions / exclusion screening
- Compliance screening concepts
- Active vs historical records
- Entity identifiers across systems
- Credentialed vs public extract access (follow current GSA/SAM documentation)

### Files to Create

```text
src/ingestion/sam_client.py
src/processing/normalize_entities.py   (extend)
data/raw/sam/
scripts/run_sam_ingestion.py
```

### Implementation Checklist

- [ ] Identify SAM public data source (API and/or extract)
- [ ] Configure API credentials in `.env` **if required** (never commit)
- [ ] **Create SAM client**
  - File: `src/ingestion/sam_client.py`
  - Depends on: settings
  - Concepts: compliance data ingestion
  - Output: download/parse client
  - Test: fetch/parse a small sample successfully
- [ ] Download exclusion records
- [ ] Parse exclusion records
- [ ] Normalize exclusion names
- [ ] Store exclusions in PostgreSQL
- [ ] Track active date
- [ ] Track termination date
- [ ] Store exclusion agency
- [ ] Store UEI when available
- [ ] Preserve source provenance
- [ ] Test SAM ingestion
- [ ] Document field mapping in data dictionary

### Definition of Done

`exclusions` table contains real public exclusion rows with normalized names and date fields; ingestion is rerunnable.

### Testing

- [ ] Count active vs terminated
- [ ] Spot-check one record against public SAM information
- [ ] Confirm secrets remain outside Git

### Common Mistakes

- Treating all historical exclusions as currently active
- Committing SAM API keys
- Matching only on raw unnormalized names
- Downloading enormous extracts before parser works on a sample

---

# Phase 8 — Entity Resolution Implementation

### Objective

Match USAspending vendors to SAM exclusions using a confidence-aware hierarchy (UEI → normalized exact name → name+location → fuzzy+geography), store auditability fields, and measure precision/recall on a labeled sample.

### Concepts to Learn

- Deterministic matching vs probabilistic/fuzzy matching
- False positives / false negatives
- Precision / recall
- Similarity scores
- Manual-review queues
- RapidFuzz token sort / partial ratios

Matching hierarchy:

1. UEI exact match
2. Normalized company-name exact match
3. Name + location
4. Fuzzy name + geography

### Files to Create

```text
src/entity_resolution/exact_match.py
src/entity_resolution/fuzzy_match.py
src/entity_resolution/entity_resolver.py
tests/test_entity_resolution.py
data/samples/entity_resolution_labeled.csv
docs/entity_resolution.md
scripts/run_entity_resolution.py
```

### Implementation Checklist

- [ ] Create / reuse company-name normalization function
- [ ] Implement exact UEI matching
- [ ] Implement exact normalized-name matching
- [ ] Implement fuzzy-name matching (RapidFuzz)
- [ ] Add city matching
- [ ] Add state matching
- [ ] Create composite match score
- [ ] Create minimum confidence threshold (auto-accept)
- [ ] Create manual-review threshold band
- [ ] Save entity matches to `entity_matches`
- [ ] Create match audit information (method, scores, inputs)
- [ ] Build small labeled test dataset
- [ ] Calculate entity-matching precision
- [ ] Calculate entity-matching recall
- [ ] Document limitations and false-positive examples
- [ ] Wire exclusion match into rules (`SAM_EXCLUSION_MATCH`) carefully

**Detailed task:**

- [ ] **Implement entity resolver orchestration**
  - File: `src/entity_resolution/entity_resolver.py`
  - Depends on: vendors + exclusions loaded
  - Concepts: matching hierarchy, confidence thresholds
  - Output: match records with audit fields
  - Test: known UEI pair matches at confidence 100; near-name non-match stays below auto-accept

### Definition of Done

Resolver runs end-to-end, persists matches with confidence/method, and reports precision/recall on a hand-labeled sample. Low-confidence matches are not auto-treated as definitive.

### Testing

- [ ] Unit tests for each match level
- [ ] Review 20 fuzzy matches manually
- [ ] Ensure “ABC TECHNOLOGIES LLC” vs “ABC TECHNOLOGY GROUP LLC” does not auto-confirm without geography/UEI support

### Common Mistakes

- Auto-accepting all fuzzy matches
- Optimizing only precision or only recall
- No audit trail
- Using DOJ defendants as if SAM exclusions were the same dataset
- Claiming “excluded” without checking active dates

---

# Phase 9 — Statistical Analytics Implementation

### Objective

Implement peer-group statistics (mean, median, std, percentiles, z-scores, IQR, MAD) and store statistical features/outlier indicators for vendors.

### Concepts to Learn

- Mean, median, variance, standard deviation
- Z-score, percentile, quartiles, IQR
- Median Absolute Deviation
- Outliers and skewed distributions
- Peer-group analysis

### Files to Create

```text
src/analytics/statistics/peer_analysis.py
src/analytics/statistics/zscores.py
tests/test_statistics.py
sql/analysis/peer_groups.sql
```

### Implementation Checklist

- [ ] Define peer groups
- [ ] Create NAICS peer groups
- [ ] Create agency peer groups
- [ ] Calculate means
- [ ] Calculate medians
- [ ] Calculate standard deviations
- [ ] Calculate percentiles
- [ ] Calculate z-scores
- [ ] Calculate IQR
- [ ] Calculate MAD
- [ ] Identify statistical outliers
- [ ] Store statistical features (DB columns or side table)
- [ ] Prefer robust measures when distributions are skewed
- [ ] Document peer definitions in methodology docs

### Definition of Done

For key metrics (growth, modification ratio, concentration, velocity), each vendor has peer-relative percentile/z/MAD indicators that can be shown in Power BI.

### Testing

- [ ] Hand-compute z-score for a tiny fixture peer group
- [ ] Confirm extreme synthetic outlier ranks at top percentile

### Common Mistakes

- Using mean/std on heavily skewed money distributions without robust alternatives
- Peer groups that are too small to be meaningful
- Interpreting z=3 as “fraud”
- Data leakage from future periods into peer baselines

---

# Phase 10 — Feature Engineering

### Objective

Build a reproducible vendor feature matrix in PostgreSQL (`vendor_features`) used by rules corroboration, statistics, ML, and scoring.

### Concepts to Learn

A **machine-learning feature** is a measurable input variable derived from raw data that a model (or rule) uses to represent an entity’s behavior.

### Feature Catalog (document each)

For every feature below, document: definition, formula, source fields, why it may matter, limitations.

```text
total_award_value
award_count
transaction_count
average_award_value
median_award_value
award_value_std
award_growth_rate
agency_count
agency_concentration
modification_count
modification_ratio
award_velocity
geographic_dispersion
set_aside_ratio
graph_degree
graph_weighted_degree
```

### Files to Create

```text
src/processing/feature_engineering.py
scripts/run_features.py
tests/test_features.py
docs/methodology.md   (feature section)
notebooks/02_feature_engineering.ipynb   (exploration only)
```

### Implementation Checklist

- [ ] Design feature schema (`vendor_features` finalized)
- [ ] **Build feature extraction pipeline**
  - File: `src/processing/feature_engineering.py`
  - Depends on: cleaned relational data
  - Concepts: feature engineering
  - Output: one row per vendor per analysis_date
  - Test: feature row counts match vendor population in scope
- [ ] Calculate financial features
- [ ] Calculate temporal features
- [ ] Calculate concentration features
- [ ] Calculate modification features
- [ ] Calculate geographic features
- [ ] Leave graph features nullable until Phase 12, then backfill
- [ ] Handle missing values explicitly
- [ ] Validate feature distributions (histograms / describe)
- [ ] Save features to PostgreSQL
- [ ] Document every feature in methodology docs
- [ ] Version the feature set (name/date in logs)

### Definition of Done

`vendor_features` is populated for the analysis population; documentation exists for each feature; notebook exploration is optional and not required to run production features.

### Testing

- [ ] Recompute a few features in SQL and compare to Python
- [ ] Assert no infinite growth rates without guards
- [ ] Null graph features do not break later ML until filled

### Common Mistakes

- Silent division by zero
- Features computed only in a notebook and never productionized
- Including target-like leakage fields
- Changing formulas without bumping analysis_date / docs
- Building ML before features are trustworthy

---

# Phase 11 — Machine-Learning Anomaly Detection

### Objective

Train an Isolation Forest on vendor features to produce anomaly scores as **one risk component**, with reproducibility, manual inspection of top anomalies, and clear documentation that scores are not fraud probabilities.

### Concepts to Learn

- Supervised vs unsupervised learning
- Anomaly detection
- Why fraud labels are unavailable
- Contamination
- Feature scaling
- Train/test concepts (carefully for unsupervised settings)
- Overfitting
- Model reproducibility / random seeds
- Selection bias (especially regarding DOJ cases)

### Files to Create

```text
src/analytics/ml/train.py
src/analytics/ml/anomaly_model.py
models/isolation_forest.joblib     (git-ignore large binaries if needed; track version metadata)
docs/ml_methodology.md
notebooks/03_anomaly_detection.ipynb
tests/test_ml_smoke.py
```

### Implementation Checklist

- [ ] Load vendor feature matrix
- [ ] Analyze distributions
- [ ] Handle missing values
- [ ] Scale features if appropriate
- [ ] **Train Isolation Forest**
  - File: `src/analytics/ml/train.py`
  - Depends on: Phase 10 features
  - Concepts: unsupervised anomaly detection
  - Output: model artifact + scores
  - Test: runs on sample matrix and returns finite scores
- [ ] Generate anomaly scores
- [ ] Rank vendors
- [ ] Inspect top anomalies manually (write notes)
- [ ] Compare model output with rule output (overlap analysis)
- [ ] Analyze model stability (seed / subsample sensitivity)
- [ ] Persist anomaly scores (into `vendor_features.anomaly_score` and/or risk components)
- [ ] Version model (params, feature list, date, seed)
- [ ] Document model assumptions
- [ ] Explicitly document that DOJ cases are **not** training labels

### Definition of Done

Every in-scope vendor has an anomaly score; top anomalies have human review notes; methodology doc explains limitations and selection bias; no resume claim of “detected fraud.”

### Testing

- [ ] Deterministic seed reproduces scores on same matrix
- [ ] Smoke test rejects empty feature matrix
- [ ] Manual review checklist completed for top N

### Common Mistakes

- Training on raw unscaled wildly different magnitude features without thought
- Treating `predict == -1` as guilt
- Tuning the model to rank known DOJ defendants higher as if that were ground truth
- No feature list versioning → unreproducible scores
- Starting ML before SQL/rules/features are solid

---

# Phase 12 — Graph Analytics Implementation

### Objective

Build a NetworkX vendor–agency bipartite graph with obligation-weighted edges, compute degree/weighted degree/centrality (and explore communities), persist graph features, and export visualization-friendly data.

### Concepts to Learn

- Graph, node, edge, weighted edge
- Bipartite graph
- Degree, weighted degree, centrality
- Community detection
- Network concentration

### Files to Create

```text
src/analytics/graph/build_graph.py
src/analytics/graph/centrality.py
src/analytics/graph/communities.py
tests/test_graph.py
notebooks/04_graph_analysis.ipynb
data/processed/graph/
```

### Implementation Checklist

- [ ] **Build NetworkX graph**
  - File: `src/analytics/graph/build_graph.py`
  - Depends on: awards/transactions + vendors + agencies
  - Concepts: bipartite graphs
  - Output: graph object + export
  - Test: small fixture graph has expected nodes/edges
- [ ] Add vendor nodes
- [ ] Add agency nodes
- [ ] Add award relationship edges
- [ ] Add obligation values as weights
- [ ] Calculate degree
- [ ] Calculate weighted degree
- [ ] Calculate centrality metrics
- [ ] Investigate community detection
- [ ] Persist graph features into `vendor_features`
- [ ] Export graph data for visualization (CSV/JSON for Power BI or Gephi)
- [ ] Document interpretation limits (centrality ≠ guilt)

### Definition of Done

Graph features exist for vendors in scope; exports available; methodology notes explain metrics.

### Testing

- [ ] Unit test on toy bipartite graph
- [ ] Spot-check one high-degree vendor against SQL distinct agency count

### Common Mistakes

- Creating a unipartite graph accidentally
- Ignoring edge weights
- Running expensive centrality on huge graphs without sampling
- Over-interpreting communities as conspiracies

---

# Phase 13 — Argus Risk Score

### Objective

Combine rules, statistical, ML, graph, and compliance components into an explainable overall Argus Risk Score with categories and per-score explanations — clearly framed as analytical ranking, not fraud probability.

### Concepts to Learn

- Score normalization / scaling
- Weighted ensembles of heterogeneous signals
- Explainability
- Risk categories as workflow prioritization tools

### Files to Create

```text
src/scoring/risk_score.py
scripts/run_scoring.py
tests/test_scoring.py
docs/risk_model.md
```

### Implementation Checklist

- [ ] Define risk components
- [ ] Normalize component scales (e.g., each to 0–100)
- [ ] Define initial weights (document them)
- [ ] Document weighting assumptions and sensitivity
- [ ] **Calculate overall score**
  - File: `src/scoring/risk_score.py`
  - Depends on: flags, stats, ML, graph, compliance outputs
  - Concepts: weighted scoring
  - Output: `risk_scores` rows + explanation payload
  - Test: known component vector produces expected overall
- [ ] Create risk categories (Low → Critical Review)
- [ ] Persist scores
- [ ] Create explanation for each score (which components drove it)
- [ ] Test edge cases (all zeros; missing ML; compliance-only)
- [ ] Ensure no score implies criminal guilt in labels/text
- [ ] Add regression tests for weight changes

### Definition of Done

Every in-scope vendor has an overall score, category, component breakdown, and human-readable explanation stored and queryable.

### Testing

- [ ] Compliance-only vendor surfaces elevated compliance component without accusing fraud
- [ ] Missing optional components degrade gracefully

### Common Mistakes

- Calling the score a “fraud probability”
- Hiding weights
- Double-counting the same signal in rules and stats without acknowledgment
- Unstable ranks when one input is null

---

# Phase 14 — DOJ Retrospective Case Studies

### Objective

Document at least two public DOJ procurement-related cases, match entities to USAspending where possible, run Argus on pre-enforcement history, and write careful case-study findings that do not claim predictive fraud detection.

### Concepts to Learn

- Retrospective validation
- Temporal cutoffs / point-in-time analysis
- Selection bias
- Case study methodology vs ML labeling

### Files to Create

```text
docs/case_studies/case_01.md
docs/case_studies/case_02.md
src/ingestion/doj_loader.py
data/raw/doj/
notebooks/05_doj_case_studies.ipynb
```

### Implementation Checklist

- [ ] Identify first DOJ case
- [ ] Document enforcement date
- [ ] Identify relevant entity
- [ ] Match entity to USAspending
- [ ] Establish analysis cutoff date
- [ ] Run historical features
- [ ] Run rules
- [ ] Run ML
- [ ] Calculate historical risk score
- [ ] Document findings (what fired, what did not, data gaps)
- [ ] Repeat for second case
- [ ] Repeat for additional cases if useful
- [ ] Store case metadata in `doj_cases`
- [ ] Explicitly state: surfacing ≠ predicting fraud

### Definition of Done

Two written case studies exist with sources, cutoff dates, Argus outputs, and limitations.

### Testing

- [ ] Peer review language for accusatory phrasing
- [ ] Confirm no post-enforcement data leaked into features

### Common Mistakes

- Using enforcement outcomes as training labels
- Cherry-picking only cases that “work”
- Ignoring missing USAspending coverage
- Writing case studies that read like guilt determinations

---

# Phase 15 — FastAPI Backend

### Objective

Expose investigation data through a documented REST API with Pydantic schemas, pagination, error handling, and tests.

### Concepts to Learn

- API, REST, endpoints, HTTP methods
- Request/response JSON
- Status codes
- Pydantic schemas
- Dependency injection
- OpenAPI / Swagger

### Files to Create

```text
src/api/main.py
src/api/routes/vendors.py
src/api/routes/awards.py
src/api/routes/analytics.py
src/api/routes/investigations.py
src/api/schemas.py
tests/test_api.py
```

### Implementation Checklist

- [ ] **Create FastAPI application**
  - File: `src/api/main.py`
  - Depends on: DB + scored data
  - Concepts: REST APIs
  - Output: runnable ASGI app
  - Test: `/health` returns 200
- [ ] Add health endpoint `GET /health`
- [ ] Create database dependency
- [ ] Create Pydantic models
- [ ] Create vendor routes (`/vendors`, `/vendors/{id}`, risk, transactions, network, exclusions)
- [ ] Create analytics routes (`/analytics/high-risk-vendors`)
- [ ] Create investigation routes (`POST /investigations/{id}/summary` stub until Phase 17)
- [ ] Add pagination
- [ ] Add error handling (404/422/500 patterns)
- [ ] Add API documentation (OpenAPI autodocs)
- [ ] Test Swagger/OpenAPI UI
- [ ] Add API tests with TestClient

### Definition of Done

Local uvicorn serves documented endpoints returning real vendor risk JSON for sample IDs.

### Testing

- [ ] pytest API suite green
- [ ] Manual Swagger checks for one vendor

### Common Mistakes

- Returning unbounded result sets
- Leaking DB exceptions to clients
- Doing heavy analytics inside request path without caching/materialization
- Skipping Pydantic validation

---

# Phase 16 — Power BI Dashboard

### Objective

Connect Power BI to PostgreSQL (or curated extracts), build investigator pages, and export screenshots for GitHub.

### Concepts to Learn

- Forensic visualization principles: clarity, provenance, prioritization, avoid sensational styling
- Semantic models / relationships
- Slicers, KPIs, tooltips
- Investigator UX vs executive vanity dashboards

### Files to Create

```text
powerbi/documentation.md
powerbi/screenshots/
```

### Implementation Checklist

- [ ] Connect Power BI to PostgreSQL
- [ ] Design semantic model
- [ ] Create vendor slicer
- [ ] Create KPI cards
- [ ] Create risk distribution
- [ ] Create time-series visualization
- [ ] Create vendor comparison page
- [ ] Create agency concentration chart
- [ ] Create modification analysis
- [ ] Create risk indicator table
- [ ] Create exclusion-screening view
- [ ] Create network visualization (or imported graph metrics)
- [ ] Add tooltips with definitions (`HIGH RISK ≠ FRAUD`)
- [ ] Add dashboard documentation
- [ ] Export screenshots for GitHub
- [ ] Build pages: Executive Overview, Vendor Investigation, Award History, Peer Comparison, Network, Exclusion Screening, Investigation Summary

### Definition of Done

An investigator can select a vendor and see score, flags, history, peers, and exclusions. Screenshots committed under `powerbi/screenshots/`.

### Testing

- [ ] Validate totals against SQL for one vendor
- [ ] Confirm filters do not double-count

### Common Mistakes

- Pretty charts with wrong grain
- No definitions for risk categories
- Publishing screenshots that imply guilt
- Connecting to prod-like DB without read-only user

---

# Phase 17 — GenAI Investigation Summaries Implementation

### Objective

Generate grounded, guardrailed investigation summaries from structured JSON findings only.

### Concepts to Learn

- LLM, prompting, hallucination, grounding
- Structured outputs
- Guardrails / safety language
- Fallback behavior when API unavailable

### Files to Create

```text
src/genai/prompts.py
src/genai/investigation_summary.py
tests/test_genai_guards.py
```

### Implementation Checklist

- [ ] Define structured investigation JSON
- [ ] Build prompt template
- [ ] Add anti-accusation guardrails
- [ ] Prevent unsupported facts (only use JSON fields)
- [ ] Connect OpenAI API via env var
- [ ] Generate investigation summary
- [ ] Validate summaries manually
- [ ] Log source indicators used
- [ ] Add fallback if API unavailable (template-based summary)
- [ ] Test hallucination scenarios (ask model to invent — ensure prompt rejects)
- [ ] Wire `POST /investigations/{id}/summary`

### Definition of Done

Summaries are produced from stored analytics, include non-accusation language, and degrade gracefully without OpenAI.

### Testing

- [ ] Unit test that prompt includes guardrail text
- [ ] Golden-file style check for template fallback
- [ ] Manual review of 10 summaries

### Common Mistakes

- Sending raw transaction dumps to the LLM
- Letting the model invent SAM matches
- No fallback path
- Committing API keys

---

# Phase 18 — Testing

### Objective

Establish a comprehensive automated test suite covering unit, integration, data validation, and end-to-end happy paths; add pytest configuration and prepare for CI.

### Concepts to Learn

- Unit tests, integration tests, end-to-end tests
- Data validation testing
- Fixtures / factories
- CI basics (GitHub Actions later)

### Files to Create

```text
tests/conftest.py
tests/test_normalization.py
tests/test_api_client.py
tests/test_loaders.py
tests/test_rules.py
tests/test_statistics.py
tests/test_entity_resolution.py
tests/test_features.py
tests/test_scoring.py
tests/test_api.py
tests/test_pipeline_e2e.py
pytest.ini or pyproject.toml tool.pytest section
.github/workflows/tests.yml   (optional late in phase)
```

### Implementation Checklist

- [ ] Test normalization functions
- [ ] Test API client (mocked HTTP)
- [ ] Test database loader (test DB or transactional fixtures)
- [ ] Test rules engine
- [ ] Test statistical calculations
- [ ] Test entity resolution
- [ ] Test feature engineering
- [ ] Test risk score
- [ ] Test FastAPI
- [ ] Test complete pipeline on sample fixtures
- [ ] Create sample fixture data under `data/samples/` / `tests/fixtures/`
- [ ] Add pytest configuration
- [ ] Add GitHub Actions later
- [ ] Enforce tests for every major analytical rule

### Definition of Done

`pytest` passes locally on a clean environment using fixtures; critical modules have coverage of happy path + key edge cases.

### Testing

- [ ] `pytest -q` exits 0
- [ ] CI green (when added)

### Common Mistakes

- Tests that hit live USAspending without mocks (flaky)
- No fixtures → slow/brittle suite
- Asserting on exact floating ranks that are unstable
- Skipping tests for “obvious” rules

---

# Phase 19 — Docker

### Objective

Containerize PostgreSQL + FastAPI with Docker Compose for reproducible startup.

### Concepts to Learn

- Container, image, Dockerfile
- Docker Compose, service, volume, network
- Environment injection into containers

### Files to Create

```text
Dockerfile
docker-compose.yml
.dockerignore
```

### Implementation Checklist

- [ ] Create Dockerfile for API/app
- [ ] Create PostgreSQL service
- [ ] Create FastAPI service
- [ ] Create persistent PostgreSQL volume
- [ ] Configure environment variables for Compose
- [ ] Create `docker-compose.yml`
- [ ] Test fresh container startup
- [ ] Document Docker commands in README setup section
- [ ] Ensure raw data volumes are intentional (do not bake secrets into images)

### Definition of Done

`docker compose up` brings up DB + API; health endpoint responds; data persists across restarts via volume.

### Testing

- [ ] Fresh machine / clean volumes path
- [ ] `curl` healthcheck
- [ ] Reboot containers and confirm volume persistence

### Common Mistakes

- Baking `.env` secrets into images
- Forgetting volumes → lost DB on restart
- Hardcoding host paths poorly
- Running as root unnecessarily without thought

---

# Phase 20 — Cloud Deployment

### Objective

Deploy only after the local system works. Keep checklist provider-neutral until AWS or Azure is selected; then implement one architecture.

### Concepts to Learn

- Managed databases, object storage, container hosting
- Secrets managers
- Network/security groups basics
- Cost control for student projects

Possible AWS architecture:

```text
S3
RDS PostgreSQL
ECS / App Runner
FastAPI
Power BI
```

Possible Azure architecture:

```text
Blob Storage
Azure Database for PostgreSQL
App Service
FastAPI
Power BI
```

### Files to Create

```text
docs/deployment.md
infra/   (optional IaC later)
```

### Implementation Checklist (provider-neutral)

- [ ] Confirm local Dockerized system is stable
- [ ] Choose cloud provider (AWS or Azure)
- [ ] Create cloud account / student credits plan
- [ ] Provision object storage for raw/processed artifacts
- [ ] Provision managed PostgreSQL
- [ ] Deploy FastAPI compute service
- [ ] Configure secrets via cloud secret store (not Git)
- [ ] Configure secure DB networking
- [ ] Connect Power BI to cloud DB (or gateway)
- [ ] Document architecture diagram for chosen provider
- [ ] Estimate monthly cost and shutdown procedure
- [ ] Smoke-test ingested sample + `/health` in cloud
- [ ] Do not claim production-grade security beyond what was implemented

### Definition of Done

A documented cloud deployment can serve the API against a managed DB using real public-data pipeline outputs (even if limited scope).

### Testing

- [ ] External healthcheck
- [ ] Credential rotation test (no secrets in repo)

### Common Mistakes

- Starting cloud before local MVP works
- Leaving expensive resources running
- Publicly exposing PostgreSQL
- Committing cloud keys

---

# Phase 21 — Documentation

### Objective

Produce complete methodology and architecture documentation suitable for portfolio reviewers and interview deep-dives.

### Files to Create

```text
docs/architecture.md
docs/data_dictionary.md
docs/methodology.md
docs/risk_model.md
docs/entity_resolution.md
docs/ml_methodology.md
docs/case_studies/
powerbi/screenshots/   (referenced)
```

### Implementation Checklist

- [ ] Architecture documentation
- [ ] Data dictionary
- [ ] Rule definitions
- [ ] Statistical methodology
- [ ] ML methodology
- [ ] Entity-resolution methodology
- [ ] Risk-score methodology
- [ ] DOJ case studies
- [ ] API documentation (link OpenAPI + narrative)
- [ ] Power BI screenshots
- [ ] Ethics disclaimer
- [ ] Dataset citations
- [ ] Sync README status checkboxes with reality

### Definition of Done

A new reader can understand what Argus does, how scores are built, what data was used, and what it does not claim — without reading all source code.

### Testing

- [ ] Have a classmate follow docs to explain the risk model back to you
- [ ] Checklist: every rule has written legitimate explanations

### Common Mistakes

- Docs that only restate code filenames
- Missing ethics language
- Inflated metrics without measurement
- Outdated screenshots

---

# Phase 22 — Portfolio Release

### Objective

Clean the repository, verify reproducibility, publish release artifacts, and prepare resume/LinkedIn language that is accurate and ethical.

### Implementation Checklist

- [ ] Clean repository
- [ ] Remove unused files
- [ ] Remove secrets (scan history if needed)
- [ ] Verify reproducible setup
- [ ] Add architecture diagram
- [ ] Add dashboard screenshots
- [ ] Add sample investigation
- [ ] Add project results (only measured metrics)
- [ ] Add dataset citations
- [ ] Add methodology documentation
- [ ] Add license
- [ ] Add resume bullets
- [ ] Add LinkedIn project description
- [ ] Create GitHub release/tag
- [ ] Have another developer follow setup instructions
- [ ] Mark all Current Project Status phases complete only if truly done

### Definition of Done

Portfolio-ready repository: reproducible, documented, ethical, demonstrable, and free of secrets.

### Testing

- [ ] Blind setup by another developer
- [ ] Secret scan clean
- [ ] Demo script runs end-to-end on sample scope

### Common Mistakes

- Claiming fraud detection on the resume
- Shipping broken setup scripts
- Leaving huge raw data in Git
- No license / no citations

---

# Concepts Learned Through Argus

Study guide: for each concept — meaning, why Argus uses it, where it appears, simple example.

## Software Engineering

### Git
1. Version control system for tracking code history  
2. Enables safe iteration on ETL/rules without losing working states  
3. Repository root; commits each phase  
4. `git commit -m "Add USAspending client"`

### Modular architecture
1. Split system into cohesive modules  
2. Keeps ingestion separate from scoring and API  
3. `src/ingestion/`, `src/analytics/`, `src/api/`  
4. Rules module imports features, not FastAPI routes

### Separation of concerns
1. Each layer has one job  
2. Prevents notebooks from becoming unmaintainable production  
3. `notebooks/` vs `src/`  
4. Exploration in notebook → function moved to `src/processing/`

### Configuration
1. Runtime settings outside code  
2. Different machines/keys without code edits  
3. `src/config/settings.py`, `.env`  
4. `DATABASE_URL=postgresql://...`

### Logging
1. Structured event records for debugging pipelines  
2. Ingestion failures must be diagnosable  
3. `src/config/logging.py`  
4. `logger.info("inserted_transactions", count=1200)`

### Testing
1. Automated verification of behavior  
2. Forensic rules must not silently break  
3. `tests/`  
4. `assert normalize_company_name(...) == ...`

### APIs
1. Programmatic interfaces over HTTP  
2. Share investigation results beyond SQL/Power BI  
3. `src/api/`  
4. `GET /vendors/1289/risk`

### Docker
1. Packaged runtime environments  
2. Reproducible Postgres+API startup  
3. `Dockerfile`, `docker-compose.yml`  
4. `docker compose up`

## Data Engineering

### ETL
1. Extract, Transform, Load pipelines  
2. Move public procurement data into PostgreSQL  
3. `src/ingestion/`, `src/processing/`  
4. API JSON → normalize → INSERT

### APIs / pagination / batch processing
1. Retrieve and process large datasets in chunks  
2. USAspending result sets exceed single responses  
3. `usaspending_client.py`  
4. Loop pages until empty

### Data normalization / schemas / validation / pipelines
1. Standardize fields and enforce structure  
2. Dirty vendor names break matching and joins  
3. `normalize_names.py`, `sql/schema.sql`  
4. `L.L.C.` → `LLC`

## Databases

### Relational database / PostgreSQL
1. Structured tables with relationships  
2. Awards/transactions need integrity and SQL analytics  
3. Phase 2 schema  
4. `awards.vendor_id → vendors.vendor_id`

### Primary keys / foreign keys / indexes / joins
1. Identity and relational links; indexes speed filters  
2. Investigator queries join vendors to obligations constantly  
3. `sql/schema.sql`, `sql/indexes.sql`  
4. `JOIN transactions t ON t.vendor_id = v.vendor_id`

### CTEs / window functions / normalization (DB)
1. Readable multi-step SQL; analytic functions over partitions  
2. YoY growth and peer ranks need windows  
3. `sql/analysis/*.sql`  
4. `LAG(annual_obligations) OVER (PARTITION BY vendor_id ORDER BY year)`

## Statistics

### Mean / median / variance / standard deviation
1. Distribution summaries  
2. Peer baselines for modification ratios etc.  
3. `src/analytics/statistics/`  
4. Peer mean modification ratio = 1.3

### Percentile / z-score / IQR / MAD / outliers / peer-group analysis
1. Relative unusualness measures; robust alternatives for skew  
2. Money data is skewed; z and MAD both useful  
3. Phase 9 modules  
4. Vendor at 99th percentile growth among NAICS peers

## Machine Learning

### Feature / model / training / inference
1. Inputs; learned function; fit; score new rows  
2. Convert procurement behavior into anomaly scores  
3. `feature_engineering.py`, `analytics/ml/`  
4. IsolationForest fit on feature matrix X

### Supervised vs unsupervised / anomaly detection / Isolation Forest
1. Labels vs no labels; find unusual points; isolation-based detector  
2. No clean fraud labels in public data  
3. Phase 11  
4. High anomaly score → review queue, not “fraud”

### Overfitting / selection bias
1. Memorizing noise; biased observed samples  
2. DOJ cases are not complete ground truth  
3. `docs/ml_methodology.md`  
4. Do not train to rank only known defendants

## Graph Theory

### Graph / node / edge / bipartite graph
1. Relationship structure between entities of two types  
2. Vendor–agency award networks  
3. `src/analytics/graph/`  
4. VendorA—Army edge weighted by obligations

### Centrality / degree / weighted degree / community
1. Importance and connectivity metrics; clusters  
2. Structural concentration indicators  
3. Phase 12  
4. Vendor degree = 12 agencies

## Forensic Analytics

### Investigative analytics / risk indicator / anomaly / alert
1. Tools to prioritize review; signals; unusualness; persisted notices  
2. Core product semantics of Argus  
3. Rules + scoring + dashboard  
4. Flag `rapid_award_growth` severity HIGH

### Entity resolution / transaction monitoring / peer analysis / compliance screening / retrospective analysis
1. Cross-dataset identity; monitoring flows; compare peers; exclusion checks; look-back validation  
2. SAM matching + rules + DOJ studies  
3. Phases 6–8, 14  
4. UEI exact match → compliance indicator

## GenAI

### LLM / prompting / grounding / structured outputs / hallucinations / guardrails
1. Large language model; instructions; tie text to facts; constrained JSON; invented facts; safety constraints  
2. Summaries must not invent misconduct  
3. `src/genai/`  
4. JSON flags in → narrative out with “does not establish misconduct”

---

# Implementation Dependency Map

```text
Repository Setup
      ↓
Data Research
      ↓
PostgreSQL
      ↓
USAspending Ingestion
      ↓
Cleaning
      ↓
SQL Analytics
      ↓
Rules Engine  --------------------→  Power BI MVP (can start)
      ↓
Feature Engineering
     ↙      ↘
Statistics   ML
     ↘      ↙
      Risk Scoring
          ↑
Graph Analytics
          ↑
SAM + Entity Resolution

Risk Scoring
      ↓
FastAPI
      ↓
Power BI (full)
      ↓
GenAI
      ↓
Testing hardening → Docker → Cloud → Docs → Portfolio
```

### What can be parallelized

- Documentation drafts while coding the same phase
- Notebook exploration alongside `src/` implementation (but promote code out of notebooks)
- Power BI mock layouts using sample extracts while rules finish
- DOJ case identification research during Phases 7–11 (execution needs scores)
- Test writing alongside each module (recommended continuous, not only Phase 18)

### What cannot be parallelized safely

- ML before trustworthy features
- GenAI before deterministic findings
- Cloud before local reproducibility
- Entity resolution before both vendors and exclusions exist
- Risk score before component inputs exist (can stub weights, but not finalize)

---

# MVP — Minimum Viable Argus

The MVP should **NOT** include everything.

## MVP Technologies

```text
Python
USAspending
PostgreSQL
SQL
Pandas
Power BI
```

## MVP Functionality

- ingest procurement records
- store vendors
- store agencies
- store awards
- store transactions
- run core SQL analyses
- implement 5 forensic rules
- calculate simple vendor risk score
- display results in Power BI

## MVP Checklist

- [ ] Phase 0 environment ready
- [ ] Agency + fiscal year scope chosen
- [ ] PostgreSQL schema for vendors/agencies/awards/transactions/risk_flags/risk_scores
- [ ] USAspending ingestion works for scope
- [ ] Cleaning/normalization for vendor names and core types
- [ ] SQL analyses: totals, growth, concentration, modifications, velocity
- [ ] Five rules implemented and persisted as flags
- [ ] Simple overall risk score from rules (weights documented)
- [ ] Power BI page(s) for vendor investigation + overview
- [ ] Ethics disclaimer visible in README and dashboard tooltip/docs
- [ ] Sample screenshots saved

```text
MVP COMPLETE WHEN:

A developer can run the ingestion pipeline,
populate PostgreSQL with real USAspending data,
select a vendor,
run five forensic analytics rules,
calculate a risk score,
and inspect the results through Power BI.
```

Only after MVP should development continue into:

```text
SAM
entity resolution
statistics
ML
graphs
DOJ validation
FastAPI
GenAI
cloud deployment
```

---

# Weekly Development Milestones

## Week 1 — Repository + USAspending research

**Deliverables:** Git repo, venv, `.gitignore`, `.env.example`, settings/logging, source notes, sample JSON, agency+FY selection.

## Week 2 — PostgreSQL + schema

**Deliverables:** `argus` DB, `sql/schema.sql`, indexes, connection module, successful test inserts/joins.

## Week 3 — USAspending ingestion

**Deliverables:** API client with pagination/retries, raw dumps, loaders for vendors/agencies/awards/transactions, ingestion stats.

## Week 4 — Cleaning + SQL analytics

**Deliverables:** normalizers + tests, data-quality report, `sql/analysis/` queries for core investigations.

## Week 5 — Rules engine

**Deliverables:** five rules, `risk_flags`, methodology writeups, rule unit tests, `run_rules.py`.

## Week 6 — Power BI MVP

**Deliverables:** connected semantic model, executive + vendor pages, screenshots, MVP completion gate met.

## Week 7 — SAM + entity resolution

**Deliverables:** exclusions loaded, matching hierarchy, `entity_matches`, precision/recall on sample, compliance flag wiring.

## Week 8 — Statistical analytics

**Deliverables:** peer groups, percentiles/z/IQR/MAD, stored statistical indicators, docs.

## Week 9 — Feature engineering + Isolation Forest

**Deliverables:** `vendor_features` pipeline, Isolation Forest scores, ML methodology doc, manual top-anomaly review notes.

## Week 10 — Graph analytics

**Deliverables:** NetworkX vendor–agency graph, degree/weighted degree/centrality features, export for viz.

## Week 11 — Risk score + DOJ cases

**Deliverables:** combined Argus score + explanations; two retrospective case study drafts.

## Week 12 — FastAPI + GenAI

**Deliverables:** documented API endpoints; grounded summary generation with guardrails + fallback.

## Week 13 — Testing + Docker

**Deliverables:** broad pytest suite; Dockerfile + compose; fresh startup verified.

## Week 14 — Documentation + portfolio release

**Deliverables:** docs complete, screenshots, citations, license, release tag, second-person setup test, resume/LinkedIn language.

---

# Development Rules

1. Make the simplest working version first.
2. Do not start machine learning before SQL analytics and feature engineering work.
3. Do not start GenAI before deterministic analytics work.
4. Do not start cloud deployment before the local system works.
5. Keep raw data separate from processed data.
6. Preserve source identifiers.
7. Never modify raw source data in place.
8. Write reusable functions instead of notebook-only logic.
9. Notebooks are for exploration, not production pipelines.
10. Put reusable code under `src/`.
11. Every major analytical rule must have tests.
12. Every risk score must be explainable.
13. Every external-data result should preserve provenance.
14. All fuzzy entity matches should preserve confidence information.
15. No API keys or passwords may enter Git.
16. Do not claim an anomaly proves fraud.
17. Do not invent performance metrics.
18. Only put metrics on the resume after measuring them.
19. Prefer interpretable analytics before complex ML.
20. The final repository must be reproducible by another developer.

---

# Setup and Installation

## Prerequisites

Install:

```text
Python 3.12+
PostgreSQL
Git
Power BI Desktop
```

Optional:

```text
Docker
```

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/argus.git
cd argus
```

## Create Virtual Environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (Git Bash / PowerShell equivalents may differ):

```bash
python -m venv .venv
source .venv/Scripts/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

Suggested initial `requirements.txt`:

```text
pandas
numpy
scipy
scikit-learn
networkx
rapidfuzz
requests
httpx
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
pydantic
openai
jupyter
matplotlib
pytest
```

## Create PostgreSQL Database

```sql
CREATE DATABASE argus;
```

Then:

```bash
psql -d argus -f sql/schema.sql
psql -d argus -f sql/indexes.sql
```

## Docker (after Phase 19)

```bash
docker compose up --build
```

---

# Environment Variables

Create `.env` (never commit it):

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/argus
USASPENDING_BASE_URL=https://api.usaspending.gov
SAM_API_KEY=YOUR_KEY_HERE
OPENAI_API_KEY=YOUR_KEY_HERE
LOG_LEVEL=INFO
```

Keep `.env.example` committed with empty placeholders only.

Add to `.gitignore`:

```text
.env
.venv/
__pycache__/
data/raw/**
!data/raw/**/.gitkeep
```

---

# Example SQL Analyses

## Vendor Award Totals

```sql
SELECT
    v.vendor_id,
    v.recipient_name,
    SUM(t.federal_action_obligation) AS total_obligations
FROM transactions t
JOIN vendors v
    ON t.vendor_id = v.vendor_id
GROUP BY
    v.vendor_id,
    v.recipient_name
ORDER BY
    total_obligations DESC;
```

## Award Growth by Fiscal Year

```sql
SELECT
    vendor_id,
    EXTRACT(YEAR FROM action_date) AS year,
    SUM(federal_action_obligation) AS annual_obligations
FROM transactions
GROUP BY
    vendor_id,
    EXTRACT(YEAR FROM action_date)
ORDER BY
    vendor_id,
    year;
```

## Vendor Agency Concentration

```sql
WITH vendor_agency AS (
    SELECT
        vendor_id,
        agency_id,
        SUM(federal_action_obligation) AS agency_obligations
    FROM transactions
    GROUP BY vendor_id, agency_id
),
vendor_totals AS (
    SELECT
        vendor_id,
        SUM(agency_obligations) AS total_obligations
    FROM vendor_agency
    GROUP BY vendor_id
)
SELECT
    va.vendor_id,
    va.agency_id,
    va.agency_obligations,
    va.agency_obligations / NULLIF(vt.total_obligations, 0) AS agency_share
FROM vendor_agency va
JOIN vendor_totals vt
    ON va.vendor_id = vt.vendor_id
ORDER BY
    agency_share DESC;
```

## Large Modification Ratios

```sql
SELECT
    award_id,
    vendor_id,
    initial_value,
    current_value,
    current_value / NULLIF(initial_value, 0) AS modification_ratio
FROM awards
WHERE initial_value > 0
ORDER BY modification_ratio DESC;
```

---

# Testing Strategy

## Unit Tests

Example:

```python
def test_normalize_company_name():
    raw = "ACME TECHNOLOGIES, L.L.C."
    expected = "ACME TECHNOLOGIES LLC"
    assert normalize_company_name(raw) == expected
```

Test normalization, rules, statistics, scoring, entity resolution, and API schemas.

## Integration Tests

```text
USAspending API (mocked or recorded)
    ↓
ETL
    ↓
PostgreSQL
    ↓
Feature calculation
```

## Data Validation

Check:

- null rates
- duplicate transaction IDs
- invalid dates
- negative values where unexpected
- missing UEIs
- inconsistent agencies
- impossible modification ratios

---

# Evaluation Metrics

Because Argus is not a traditional binary fraud classifier, evaluation should use multiple metrics. **Do not invent metrics for the resume.**

## Data Pipeline

- records ingested
- API failure rate
- duplicate rate
- missing-field rate
- ingestion runtime

## Entity Resolution

- precision
- recall
- manual-review accuracy
- exact vs fuzzy-match rates

## Anomaly Detection

- anomaly stability
- percentile ranking
- known-case ranking (retrospective only; not training target)
- feature contribution analysis

## Rules Engine

- number of flags generated
- false-positive review rate (manual)
- overlap between rules
- distribution across peer groups

## Historical Validation

For each DOJ case:

```text
Percentile rank before enforcement
Number of triggered rules
ML anomaly score
Overall Argus risk score
```

---

# Ethical and Investigative Limitations

This project must clearly state its limitations.

## Argus Does Not Determine Guilt

An anomaly is not evidence of fraud.

Possible explanations for unusual procurement behavior include:

- emergency contracting
- legitimate rapid company growth
- specialized supplier relationships
- contract scope changes
- disaster response
- industry structure
- government policy changes

Therefore:

```text
HIGH RISK ≠ FRAUD
ANOMALY ≠ MISCONDUCT
```

The appropriate interpretation is:

```text
HIGH RISK = PRIORITY FOR FURTHER REVIEW
```

## Public Data Limitations

Government datasets may include delayed reporting, incomplete information, inconsistent identifiers, corrected transactions, missing fields, and reporting errors. All findings should be presented with appropriate uncertainty.

## Entity Matching Limitations

Fuzzy matching can produce false positives.

Example:

```text
ABC TECHNOLOGIES LLC
ABC TECHNOLOGY GROUP LLC
```

High name similarity does not guarantee identical organizations. Low-confidence matches require human verification.

## Model Bias / Selection Bias

Known enforcement cases represent only misconduct that was detected, investigated, and resulted in public enforcement. They are not a representative sample of all procurement behavior and must not be treated as a comprehensive labeled fraud dataset.

---

# Security and Data Handling

Although Argus uses public information, development should follow good security practices.

Do not commit:

```text
API keys
database passwords
cloud secrets
private credentials
```

Use:

```text
.env
secret managers
environment variables
```

Prefer read-only DB users for Power BI. Do not expose PostgreSQL to the public internet without deliberate hardening.

---

# Potential Resume Bullets

Only use metrics after they have actually been measured.

## Project Header

**Argus — Federal Procurement Risk & Forensic Analytics**  
*Python, PostgreSQL, SQL, Pandas, scikit-learn, NetworkX, Power BI, FastAPI*

Potential bullets:

- Engineered a forensic analytics pipeline integrating USAspending procurement transactions and SAM.gov exclusion data to identify anomalous contractor activity using Python, SQL, statistical analysis, and rules-based detection

- Developed vendor risk features across award growth, contract modifications, agency concentration, transaction velocity, and peer-group behavior to prioritize entities for investigative review

- Built unsupervised anomaly-detection and graph-analysis workflows with scikit-learn and NetworkX to surface statistically unusual procurement behavior and vendor-agency relationships

- Designed an interactive Power BI investigation dashboard combining transaction history, anomaly scores, compliance screening, and explainable risk indicators

- Conducted retrospective case analyses using publicly documented DOJ enforcement actions to evaluate whether unusual procurement patterns were visible before enforcement announcements

Do not claim:

```text
detected fraud
prevented fraud
identified criminals
```

unless such claims can actually be supported.

---

# Interview Talking Points

## 30-Second Explanation

> Argus is a forensic analytics platform I built using real federal procurement data from USAspending, SAM.gov exclusion records, and public DOJ enforcement cases. The system combines SQL-based investigative rules, statistical peer analysis, machine-learning anomaly detection, and graph analytics to identify unusual contractor behavior and prioritize entities for further review. I also built a Power BI investigation dashboard and use GenAI only to summarize structured analytical findings rather than make unsupported conclusions.

## Why Use Public Procurement Data?

> I wanted the project to use real transactional data rather than a synthetic fraud dataset. Federal procurement data gives me millions of real-world financial records while still allowing the entire project to remain reproducible and publicly shareable.

## Why Anomaly Detection Instead of Fraud Classification?

> Public procurement data doesn't provide a reliable ground-truth label for every vendor. A supervised fraud classifier would create misleading assumptions. I therefore treated the problem as anomaly detection and investigative prioritization.

## Why Use Rules and ML Together?

> Rules are interpretable and useful when investigators know the pattern they want to test. Machine learning can identify unusual combinations that predefined rules may miss. Combining both provides better analytical coverage while preserving explainability.

## What Was the Hardest Technical Problem?

> Entity resolution was one of the most difficult parts because company names differ across government datasets. I implemented a hierarchy using UEIs, normalized names, geographic attributes, and fuzzy matching while preserving confidence scores for review.

## How Does GenAI Fit?

> The LLM does not determine risk. The analytical engine calculates the indicators first. GenAI receives structured facts and converts them into an investigator-readable summary with guardrails preventing unsupported accusations.

---

# Stretch Goals

Once the core system works, consider adding:

## SEC Data

Integrate SEC EDGAR for publicly traded federal contractors (financial condition, procurement revenue concentration, material disclosures).

## Lobbying Data

Research public lobbying disclosures and compare with procurement trends — carefully, never implying causation from correlation alone.

## Subaward Networks

Analyze prime → subcontractor relationships for richer graphs.

## Natural-Language Search

Allow controlled analytical queries from investigator language (translated into constrained SQL/API calls — not freeform LLM database access).

## Time-Series Models

Change-point detection, forecasting, seasonality analysis for sudden behavior shifts.

## Explainable ML

Add SHAP or similar methods to identify feature contributions to anomaly scores.

## Cloud Pipeline

AWS: S3 → Python ingestion → RDS PostgreSQL → FastAPI → Power BI  

Azure: Blob Storage → Azure Functions → Azure Database for PostgreSQL → FastAPI → Power BI

## Scheduled Monitoring

Recurring ingestion jobs and recomputed vendor risk scores as new procurement data arrives.

---

# Final Definition of Done

The complete Argus project is finished when:

- [ ] real USAspending data can be ingested automatically
- [ ] data is stored in PostgreSQL
- [ ] vendors, agencies, awards, and transactions are relationally linked
- [ ] data quality checks run successfully
- [ ] at least five rules-based risk indicators work
- [ ] SAM exclusions are ingested
- [ ] entity resolution works
- [ ] statistical peer analysis works
- [ ] vendor features are generated
- [ ] Isolation Forest produces anomaly scores
- [ ] graph analytics produces vendor network features
- [ ] Argus produces explainable overall risk scores
- [ ] at least two DOJ retrospective case studies are documented
- [ ] FastAPI exposes analytical results
- [ ] Power BI provides an investigator dashboard
- [ ] GenAI generates grounded investigation summaries
- [ ] automated tests pass
- [ ] Docker can start the application
- [ ] setup instructions work on a clean machine
- [ ] no credentials exist in the repository
- [ ] ethical limitations are documented
- [ ] architecture documentation is complete
- [ ] dashboard screenshots are included
- [ ] measurable results are documented
- [ ] project is ready to place on a resume

Related earlier checklist (portfolio readiness): documented sources, reproducible ingestion, schema, SQL investigations, rules, stats, SAM matching, ML scores, graph analysis, risk methodology, case studies, screenshots, API examples, tests, architecture diagram, methodology docs, ethics disclaimer, clear README, measured results.

---

# References

## USAspending

USAspending.gov  
https://www.usaspending.gov/

USAspending API  
https://api.usaspending.gov/

## SAM.gov / GSA

SAM.gov  
https://sam.gov/

Open GSA APIs  
https://open.gsa.gov/

## Department of Justice

U.S. Department of Justice  
https://www.justice.gov/

Procurement Collusion Strike Force  
https://www.justice.gov/atr/procurement-collusion-strike-force

---

# Disclaimer

Argus is an educational and portfolio project.

It uses publicly available data to demonstrate data engineering, forensic analytics, statistical analysis, machine learning, and investigative visualization techniques.

Risk scores and anomaly indicators generated by Argus are analytical signals only.

They do not establish fraud, misconduct, regulatory violations, criminal activity, or legal liability.

Any real-world investigative conclusion would require additional evidence, context, subject-matter expertise, and appropriate legal or compliance review.

```text
HIGH RISK ≠ FRAUD
ANOMALY ≠ MISCONDUCT
```

---

# Author

**Santiago Rubio Bolaños**  
Computer Science  
Texas State University

---

## Project Vision

Argus should ultimately demonstrate one core idea:

> **Use real public financial data to transform millions of procurement records into explainable investigative signals that help analysts decide where to look next.**
