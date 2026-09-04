# Argus Data Dictionary (Draft)

Status: **Phase 1 draft** — refine as ingestion and schema solidify.

Initial development scope (see [`sources_notes.md`](sources_notes.md)):

```text
Agency: National Aeronautics and Space Administration (NASA)
Fiscal Year: 2024 (2023-10-01 → 2024-09-30)
Award types: contracts A/B/C/D
```

---

## Entity Overview

| Entity | Grain | Likely primary key | Source |
|---|---|---|---|
| Vendor / Recipient | One organization | `vendor_id` (internal) + `recipient_uei` when present | USAspending recipient fields |
| Agency | Toptier / subtier | `agency_id` (internal) + agency codes/names | Awarding / funding agency objects |
| Award | One award | `generated_unique_award_id` / award `id` | `/api/v2/awards/{id}/`, spending_by_award |
| Transaction | One federal action | transaction `id` / action row | `/api/v2/transactions/`, spending_by_transaction |
| Exclusion | One SAM exclusion record | SAM native id + UEI/name | SAM.gov / GSA extracts |
| DOJ case | One enforcement announcement | `case_id` (internal) | Public DOJ pages |

---

## USAspending — Awards (search response)

Observed in `data/samples/usaspending/sample_awards_response.json`:

| Field | Type (approx) | Null-prone? | Notes |
|---|---|---|---|
| `Award ID` | string | low | Display / PIID-like identifier; **not** always globally unique alone |
| `generated_internal_id` | string | low | Strong candidate natural key (`CONT_AWD_...`) |
| `internal_id` | integer | low | USAspending internal award id |
| `Recipient Name` | string | low | Dirty; needs normalization |
| `Recipient UEI` | string | **medium/high** | Best vendor join key when present |
| `Award Amount` | number | medium | Search field; confirm vs obligation fields on detail |
| `Start Date` / `End Date` | date string | medium | Period of performance |
| `Awarding Agency` | string | low | Toptier display name |
| `Awarding Sub Agency` | string | medium | Subtier name |
| `awarding_agency_id` | integer | medium | Useful FK candidate |
| `Funding Agency` / `Funding Sub Agency` | string | medium | May differ from awarding |
| `Contract Award Type` | string | medium | Contract category label |
| `Description` | text | high | Free text; useful for investigation, not joins |
| `agency_slug` | string | medium | URL-friendly agency slug |

### Award detail extras

Observed in `sample_award_detail.json`:

| Field | Notes |
|---|---|
| `generated_unique_award_id` | Preferred natural award key |
| `piid` | Procurement instrument ID |
| `recipient.uei` / `recipient.recipient_name` | Vendor identifiers |
| `recipient.location.*` | City/state/country for matching |
| `awarding_agency` / `funding_agency` objects | Nested toptier/subtier codes & names |
| `naics_hierarchy` / `psc_hierarchy` | Peer-group dimensions |
| `total_obligation` / `base_and_all_options` / `base_exercised_options` | Money fields for modification analysis |
| `period_of_performance` | Start/end dates |
| `latest_transaction_contract_data` | Contract-specific attributes |
| `place_of_performance` | Geography |

---

## USAspending — Transactions

Observed in `sample_transactions_response.json` / `sample_transactions_by_award.json`:

| Field | Notes |
|---|---|
| `Award ID` | Links conceptually to award |
| `Action Date` / `action_date` | Temporal analysis key |
| `Transaction Amount` / `federal_action_obligation` | Obligation for the action |
| `Mod` / `modification_number` | Modification indicator |
| `Recipient Name` | May differ slightly from award-level name |
| `Awarding Agency` / Sub Agency | Action-level agency context |
| `generated_internal_id` | Award linkage |
| `id` (transaction) | Candidate transaction PK from `/api/v2/transactions/` |
| `action_type` / `action_type_description` | Why the action occurred |
| `description` | Action narrative |

**Grain warning:** do not mix award totals and transaction sums without care — double-counting is easy.

---

## Proposed Argus relational mapping (forward look)

| Argus table | Source fields |
|---|---|
| `vendors` | UEI, recipient name, location |
| `agencies` | toptier/subtier codes + names |
| `awards` | generated unique award id, vendor FK, agency FKs, NAICS/PSC, values, dates |
| `transactions` | transaction id, award FK, action date, obligation, modification number |
| `exclusions` | SAM UEI/name/dates/type |
| `doj_cases` | title, entity, enforcement date, URL |

---

## Vendor identifiers

Priority for joins / entity resolution:

1. UEI (exact)
2. Normalized recipient name
3. Name + city/state
4. Fuzzy name + geography (RapidFuzz later)

---

## Agency identifiers

- Toptier agency name / abbreviation / code
- Subtier agency name / abbreviation / code
- `awarding_agency_id` from search results when available

---

## Null-heavy / fragile fields (watchlist)

- Recipient UEI missing on some recipients
- Description often sparse or generic
- Funding vs awarding agency mismatches / blanks
- Initial vs current award values depending on endpoint
- Modification numbers that are non-numeric strings

---

## SAM.gov exclusions (to refine in Phase 7)

Expected concepts:

- Entity name / aliases
- UEI (when available)
- Exclusion type / program
- Excluding agency
- Active date / termination date
- Address / city / state / country

Active vs terminated must be tracked separately.

---

## DOJ cases (to refine in Phase 14)

Capture:

- Case title
- Entity / defendant name(s)
- Enforcement / announcement date
- Source URL
- Short summary
- Notes for Argus cutoff date

---

## Open questions

- [ ] Confirm best stable award PK for upserts (`generated_unique_award_id` vs internal numeric `id`)
- [ ] Confirm transaction PK from POST `/api/v2/transactions/`
- [ ] Decide how to store nested agency JSON vs flattened agency table
- [ ] Document bulk-download column names vs API field labels (they differ)
