# Argus Data Quality Report

Generated: `2026-09-07T06:23:39.808213+00:00`  
Dry run: `False`

> Raw files under `data/raw/` are never modified by Phase 4 tooling.

## Vendor metrics

| Metric | Value |
| --- | ---: |
| Vendors scanned | 5 |
| `normalized_name` updated | 3 |
| `normalized_name` unchanged | 2 |
| UEI OK | 5 |
| UEI missing | 0 |
| UEI invalid format | 0 |
| Reject log entries | 0 |
| Duplicate normalized names | 1 |

## Reject log

Path: `data/processed/vendors/vendor_rejects_20260907_062339.json`

## Duplicate normalized names (sample)

- `THE BOEING CO` × 2

## Notes

- `normalize_company_name` uppercases names and canonicalizes LLC/INC/CORP-style suffixes.
- Invalid or missing UEIs are logged; rows are not deleted.
- Re-run: `python scripts/run_normalization.py`
