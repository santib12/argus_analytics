-- =============================================================================
-- Argus Phase 2 — sql/indexes.sql
-- =============================================================================
-- PURPOSE
--   Speed up common joins and filters used by SQL analytics / Power BI / API.
--
-- WHEN TO RUN
--   AFTER sql/schema.sql succeeds:
--     psql -d argus -f sql/indexes.sql
--
-- INDEXING GUIDANCE
--   - Index foreign keys you join on frequently.
--   - Index columns used in WHERE / ORDER BY for investigator queries.
--   - Do NOT index every column (writes get slower; planner can get confused).
--   - Revisit indexes after you write Phase 5 SQL and notice slow queries.
-- =============================================================================

-- Vendors
-- TODO: implement / uncomment after schema exists
CREATE INDEX IF NOT EXISTS idx_vendors_uei
    ON vendors (recipient_uei);

CREATE INDEX IF NOT EXISTS idx_vendors_normalized_name
    ON vendors (normalized_name);

-- Agencies
CREATE INDEX IF NOT EXISTS idx_agencies_code
    ON agencies (agency_code);

CREATE INDEX IF NOT EXISTS idx_agencies_name
    ON agencies (agency_name);

-- Awards
CREATE INDEX IF NOT EXISTS idx_awards_vendor
    ON awards (vendor_id);

CREATE INDEX IF NOT EXISTS idx_awards_awarding_agency
    ON awards (awarding_agency_id);

CREATE INDEX IF NOT EXISTS idx_awards_funding_agency
    ON awards (funding_agency_id);

CREATE INDEX IF NOT EXISTS idx_awards_naics
    ON awards (naics_code);

CREATE INDEX IF NOT EXISTS idx_awards_psc
    ON awards (product_service_code);

-- Transactions (very common analytical filters)
CREATE INDEX IF NOT EXISTS idx_transactions_vendor
    ON transactions (vendor_id);

CREATE INDEX IF NOT EXISTS idx_transactions_award
    ON transactions (award_id);

CREATE INDEX IF NOT EXISTS idx_transactions_action_date
    ON transactions (action_date);

CREATE INDEX IF NOT EXISTS idx_transactions_agency
    ON transactions (agency_id);

-- Exclusions / matching
CREATE INDEX IF NOT EXISTS idx_exclusions_uei
    ON exclusions (uei);

CREATE INDEX IF NOT EXISTS idx_exclusions_normalized_name
    ON exclusions (normalized_name);

CREATE INDEX IF NOT EXISTS idx_entity_matches_vendor
    ON entity_matches (vendor_id);

CREATE INDEX IF NOT EXISTS idx_entity_matches_exclusion
    ON entity_matches (exclusion_id);

-- Risk / features
CREATE INDEX IF NOT EXISTS idx_risk_flags_vendor
    ON risk_flags (vendor_id);

CREATE INDEX IF NOT EXISTS idx_risk_flags_type
    ON risk_flags (flag_type);

CREATE INDEX IF NOT EXISTS idx_risk_scores_overall
    ON risk_scores (overall_score DESC);

-- =============================================================================
-- OPTIONAL LATER
--   - Partial index on active exclusions: WHERE termination_date IS NULL
--   - Composite index (vendor_id, action_date) if YoY queries are hot
-- =============================================================================
