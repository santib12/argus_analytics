# Argus Source Notes (Phase 1)

Research log for public data sources used by Argus.

Last updated: 2026-09-03

---

## Initial development dataset (selected)

```text
ONE agency:  National Aeronautics and Space Administration (NASA)
ONE FY:      FY2024
Window:      2023-10-01 → 2024-09-30
Award types: Contracts A, B, C, D
```

**Why this scope**

- Large enough to be realistic
- Smaller than DoD-wide extracts
- Easy to reason about while building ETL
- Matches README guidance: one agency + one fiscal year first

Expand later only after ingestion/cleaning/rules work on this slice.

---

## USAspending

### Official links

- Site: https://www.usaspending.gov/
- API base: https://api.usaspending.gov
- Intro tutorial: https://api.usaspending.gov/docs/intro-tutorial
- Endpoint index: https://api.usaspending.gov/docs/endpoints
- API contracts (GitHub): https://github.com/fedspendingtransparency/usaspending-api

### Relevant endpoints (initial)

| Method | Endpoint | Purpose for Argus |
|---|---|---|
| POST | `/api/v2/search/spending_by_award/` | Search awards with agency + time filters |
| POST | `/api/v2/search/spending_by_transaction/` | Search transactions / actions |
| GET | `/api/v2/awards/{award_id}/` | Award detail (recipient, NAICS/PSC, obligations) |
| POST | `/api/v2/transactions/` | Paginated transactions for an award (`award_id`) |
| GET | `/api/v2/awards/last_updated/` | Freshness check |
| POST | `/api/v2/search/spending_by_award_count/` | Count awards before large pulls |

Notes:

- Advanced search endpoints are usually **POST + JSON body** (not simple GET query strings).
- Pagination uses `page` / `limit` (and related metadata).
- `sort` can be required on some search endpoints (observed on spending_by_transaction).
- Always save raw JSON under `data/raw/` in Phase 3; Phase 1 keeps tiny samples under `data/samples/`.

### Example award search body (NASA FY2024)

```json
{
  "filters": {
    "award_type_codes": ["A", "B", "C", "D"],
    "time_period": [{"start_date": "2023-10-01", "end_date": "2024-09-30"}],
    "agencies": [
      {
        "type": "awarding",
        "tier": "toptier",
        "name": "National Aeronautics and Space Administration"
      }
    ]
  },
  "fields": [
    "Award ID",
    "Recipient Name",
    "Recipient UEI",
    "Start Date",
    "End Date",
    "Award Amount",
    "Awarding Agency",
    "Awarding Sub Agency",
    "Contract Award Type",
    "Funding Agency",
    "Funding Sub Agency",
    "Description"
  ],
  "limit": 5,
  "page": 1,
  "sort": "Award Amount",
  "order": "desc"
}
```

### Bulk downloads

USAspending also publishes bulk award/transaction files (CSV/zip) for large historical loads.

Phase 1 stance:

- Use API samples for schema discovery
- Prefer API for controlled agency+FY MVP
- Revisit bulk files when scaling beyond interactive API pagination

Document exact bulk file names/URLs when first used in Phase 3.

### Sample files captured

Directory: `data/samples/usaspending/`

| File | Contents |
|---|---|
| `provenance.json` | Download date, filters, endpoints |
| `sample_awards_response.json` | POST spending_by_award page (limit 5) |
| `sample_awards.csv` | Flattened award rows |
| `sample_award_detail.json` | GET award detail for one award |
| `sample_transactions_response.json` | POST spending_by_transaction (limit 5) |
| `sample_transactions_by_award.json` | POST `/api/v2/transactions/` for one award |

### Observed keys / relationships

```text
Award.generated_unique_award_id / generated_internal_id
   ↓
Award.internal_id / id
   ↓
Transactions (award_id / generated_internal_id)
   ↓
Recipient (UEI, name, location)
Agency (awarding / funding toptier + subtier)
```

Primary-key candidates:

- Award: `generated_unique_award_id` (preferred natural), numeric `id` (internal)
- Transaction: transaction `id` from `/api/v2/transactions/`
- Vendor: UEI when present; else normalized name (+ geography)

Null-prone:

- UEI
- descriptions
- some funding agency fields
- optional hierarchy fields

---

## SAM.gov exclusions / GSA

### Links

- SAM.gov: https://sam.gov/
- Open GSA APIs: https://open.gsa.gov/

### What to capture later (Phase 7)

- Exclusion entity name + aliases
- UEI
- Exclusion type / program
- Excluding agency
- Active date / termination date
- Address fields

### Identifiers for matching

1. UEI exact
2. Normalized name exact
3. Name + location
4. Fuzzy name + geography (with confidence)

Track **active vs historical** exclusions explicitly.

API credentials (if required) go in `.env` as `SAM_API_KEY` — never in Git.

---

## Department of Justice cases

### Links

- DOJ: https://www.justice.gov/
- Procurement Collusion Strike Force: https://www.justice.gov/atr/procurement-collusion-strike-force

### How Argus will use cases

- Retrospective validation only
- **Not** complete fraud labels for supervised ML
- Store announcement date → analysis cutoff before enforcement

Candidate sources:

- DOJ press releases mentioning procurement / contracting fraud
- PCSF announcements
- Public case summaries

Store structured notes eventually in `docs/case_studies/` and `doj_cases` table.

---

## Concepts checklist (learning notes)

- REST API / JSON / pagination
- HTTP GET vs POST
- Timeouts, retries, polite rate usage
- UEI, NAICS, PSC
- Awards vs transactions vs modifications
- Fiscal year vs calendar year windows

---

## Next actions after Phase 1 files

1. Walk through `notebooks/01_data_exploration.ipynb`
2. Flesh null-rate notes after inspecting samples
3. Lock award/transaction PK decisions into `sql/schema.sql` (Phase 2)
