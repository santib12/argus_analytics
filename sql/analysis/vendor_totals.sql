-- =============================================================================
-- Argus Phase 5 — sql/analysis/vendor_totals.sql
-- =============================================================================
-- PURPOSE
--   One row per vendor with award counts, transaction counts, and total
--   federal action obligations. This is the first investigator baseline query.
--
-- GRAIN
--   One row per vendors.vendor_id
--
-- WHY THIS MATTERS
--   Forensic work usually starts with: who got how much, how many awards,
--   and how many transaction actions? Mixing award grain vs transaction grain
--   incorrectly is the #1 SQL mistake in procurement analytics.
--
-- CONCEPTS
--   JOIN, LEFT JOIN, GROUP BY, COUNT(DISTINCT ...), COALESCE(SUM(...), 0)
--
-- IMPORTANT
--   Prefer SUM(transactions.federal_action_obligation) for "money moved".
--   Do NOT assume SUM(transactions) == awards.current_value.
--
-- HOW TO RUN
--   PGPASSWORD=password psql -h localhost -U argus -d argus \
--     -f sql/analysis/vendor_totals.sql
-- =============================================================================

SELECT
    v.vendor_id,
    v.recipient_name,
    v.normalized_name,
    v.recipient_uei,

    COUNT(DISTINCT a.award_id) AS award_count,
    COUNT(DISTINCT t.transaction_id) AS transaction_count,
    COALESCE(SUM(t.federal_action_obligation),0) AS total_obligations

FROM vendors v
LEFT JOIN awards a
    ON a.vendor_id = v.vendor_id

LEFT JOIN transactions t
    ON t.award_id = a.award_id

GROUP BY
    v.vendor_id,
    v.recipient_name,
    v.normalized_name,
    v.recipient_uei


ORDER BY
    total_obligations DESC
