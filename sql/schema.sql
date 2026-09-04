-- =============================================================================
-- Argus Phase 2 — sql/schema.sql
-- =============================================================================
-- PURPOSE
--   Define the relational schema for vendors, agencies, awards, transactions,
--   exclusions, entity matches, features, risk flags/scores, and DOJ cases.
--
-- HOW TO USE THIS FILE
--   1. Install PostgreSQL locally.
--   2. Create database:  CREATE DATABASE argus;
--   3. Apply schema:     psql -d argus -f sql/schema.sql
--   4. Then apply:       psql -d argus -f sql/indexes.sql
--
-- If tables already exist with an older shape, drop them first (dev only):
--   DROP TABLE IF EXISTS risk_scores, risk_flags, vendor_features, entity_matches,
--     transactions, awards, exclusions, doj_cases, agencies, vendors CASCADE;
--
-- DESIGN RULES
--   - Prefer REAL types: DATE for dates, NUMERIC for money, TIMESTAMPTZ for timestamps.
--   - Do NOT use vendor/recipient NAME as a primary key.
--   - Preserve source identifiers from USAspending (UEI, generated_unique_award_id).
--   - Derived analytics tables should include analysis_date.
--   - HIGH RISK ≠ FRAUD — these tables store analytical signals, not guilt.
-- =============================================================================

-- Optional rebuild helpers (DEV ONLY — keep commented for normal runs):
-- DROP TABLE IF EXISTS risk_scores CASCADE;
-- DROP TABLE IF EXISTS risk_flags CASCADE;
-- DROP TABLE IF EXISTS vendor_features CASCADE;
-- DROP TABLE IF EXISTS entity_matches CASCADE;
-- DROP TABLE IF EXISTS transactions CASCADE;
-- DROP TABLE IF EXISTS awards CASCADE;
-- DROP TABLE IF EXISTS exclusions CASCADE;
-- DROP TABLE IF EXISTS doj_cases CASCADE;
-- DROP TABLE IF EXISTS agencies CASCADE;
-- DROP TABLE IF EXISTS vendors CASCADE;

CREATE TABLE IF NOT EXISTS vendors (
    vendor_id           BIGSERIAL PRIMARY KEY,
    recipient_uei       VARCHAR(12),
    recipient_name      TEXT NOT NULL,
    normalized_name     TEXT,
    city                TEXT,
    state               VARCHAR(2),
    country             TEXT,
    zip_code            VARCHAR(20),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_vendors_uei UNIQUE (recipient_uei)
);

CREATE TABLE IF NOT EXISTS agencies (
    agency_id           BIGSERIAL PRIMARY KEY,
    agency_code         VARCHAR(20),
    agency_name         TEXT NOT NULL,
    subtier_agency_name TEXT,
    CONSTRAINT uq_agencies_code_name
        UNIQUE (agency_code, agency_name, subtier_agency_name)
);

CREATE TABLE IF NOT EXISTS awards (
    award_id                    TEXT PRIMARY KEY,
    usaspending_internal_id     BIGINT,
    vendor_id                   BIGINT NOT NULL REFERENCES vendors(vendor_id),
    awarding_agency_id          BIGINT REFERENCES agencies(agency_id),
    funding_agency_id           BIGINT REFERENCES agencies(agency_id),
    award_type                  TEXT,
    description                 TEXT,
    naics_code                  VARCHAR(10),
    product_service_code        VARCHAR(10),
    start_date                  DATE,
    end_date                    DATE,
    initial_value               NUMERIC(20, 2),
    current_value               NUMERIC(20, 2),
    potential_value             NUMERIC(20, 2),
    place_of_performance_state  VARCHAR(2),
    set_aside_type              TEXT,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id              TEXT PRIMARY KEY,
    award_id                    TEXT NOT NULL REFERENCES awards(award_id),
    vendor_id                   BIGINT REFERENCES vendors(vendor_id),
    agency_id                   BIGINT REFERENCES agencies(agency_id),
    action_date                 DATE NOT NULL,
    federal_action_obligation   NUMERIC(20, 2),
    current_total_value         NUMERIC(20, 2),
    potential_total_value       NUMERIC(20, 2),
    modification_number         TEXT,
    description                 TEXT,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS exclusions (
    exclusion_id        BIGSERIAL PRIMARY KEY,
    uei                 VARCHAR(12),
    entity_name         TEXT NOT NULL,
    normalized_name     TEXT,
    exclusion_type      TEXT,
    excluding_agency    TEXT,
    active_date         DATE,
    termination_date    DATE,
    address             TEXT,
    city                TEXT,
    state               VARCHAR(2),
    country             TEXT,
    source_system       TEXT DEFAULT 'SAM.gov',
    downloaded_at       TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS entity_matches (
    match_id            BIGSERIAL PRIMARY KEY,
    vendor_id           BIGINT NOT NULL REFERENCES vendors(vendor_id),
    exclusion_id        BIGINT NOT NULL REFERENCES exclusions(exclusion_id),
    match_type          TEXT NOT NULL,
    similarity_score    NUMERIC(6, 2),
    uei_match           BOOLEAN,
    name_match          BOOLEAN,
    address_match       BOOLEAN,
    review_status       TEXT NOT NULL DEFAULT 'pending',
    CONSTRAINT ck_entity_matches_review_status
        CHECK (review_status IN ('pending', 'accepted', 'rejected')),
    CONSTRAINT uq_entity_matches_vendor_exclusion_type
        UNIQUE (vendor_id, exclusion_id, match_type)
);

CREATE TABLE IF NOT EXISTS vendor_features (
    vendor_id                   BIGINT NOT NULL REFERENCES vendors(vendor_id),
    analysis_date               DATE NOT NULL,
    total_award_value           NUMERIC(20, 2),
    award_count                 INTEGER,
    transaction_count           INTEGER,
    average_award_value         NUMERIC(20, 2),
    median_award_value          NUMERIC(20, 2),
    award_value_std             NUMERIC(20, 2),
    award_growth_rate           NUMERIC(12, 6),
    agency_count                INTEGER,
    agency_concentration        NUMERIC(8, 6),
    modification_count          INTEGER,
    average_modification_ratio  NUMERIC(12, 6),
    award_velocity              NUMERIC(12, 6),
    geographic_count            INTEGER,
    set_aside_ratio             NUMERIC(8, 6),
    graph_degree                INTEGER,
    graph_weighted_degree       NUMERIC(20, 2),
    anomaly_score               NUMERIC(12, 6),
    PRIMARY KEY (vendor_id, analysis_date)
);

CREATE TABLE IF NOT EXISTS risk_flags (
    risk_flag_id        BIGSERIAL PRIMARY KEY,
    vendor_id           BIGINT NOT NULL REFERENCES vendors(vendor_id),
    award_id            TEXT REFERENCES awards(award_id),
    flag_type           TEXT NOT NULL,
    severity            TEXT NOT NULL,
    score               NUMERIC(8, 2),
    description         TEXT NOT NULL,
    detected_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    evidence            JSONB,
    CONSTRAINT ck_risk_flags_severity
        CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH'))
);

CREATE TABLE IF NOT EXISTS risk_scores (
    vendor_id           BIGINT NOT NULL REFERENCES vendors(vendor_id),
    analysis_date       DATE NOT NULL,
    rules_score         NUMERIC(8, 2),
    statistical_score   NUMERIC(8, 2),
    ml_score            NUMERIC(8, 2),
    graph_score         NUMERIC(8, 2),
    compliance_score    NUMERIC(8, 2),
    overall_score       NUMERIC(8, 2) NOT NULL,
    risk_level          TEXT NOT NULL,
    PRIMARY KEY (vendor_id, analysis_date)
);

CREATE TABLE IF NOT EXISTS doj_cases (
    case_id                     BIGSERIAL PRIMARY KEY,
    case_title                  TEXT NOT NULL,
    defendant_or_entity_name    TEXT NOT NULL,
    normalized_name             TEXT,
    enforcement_date            DATE,
    agency_or_component         TEXT,
    case_url                    TEXT,
    summary                     TEXT,
    notes                       TEXT,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
