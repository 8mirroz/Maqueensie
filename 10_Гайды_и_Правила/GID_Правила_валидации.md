---
doc_id: validation_rules
doc_type: policy
status: active
date_added: 2026-04-17
date_verified: 2026-04-17
tags: [validation, policy]

title: "Правила валидации"---

# Validation Rules

## YAML Contracts (tiered strictness)

Validator applies contract by note shape:
- `legacy_strict`: old competitor/pricing cards (`competitor`/`service_type`/`price_tier` markers or legacy filename pattern `YYYY-MM-DD_*`)
- `content_core`: new analytical notes (market maps, demand maps, catalogs, offers, etc.)
- `doc_core`: system/architecture reports (`doc_id` + `doc_type`)

### Contract A — `legacy_strict` (full normalization)

```yaml
domain: ["Architecture", "Interior", "Renovation", "Decor", "Furniture", "RealEstate"]
subdomain: ["String"]
competitor: "String"
service_type: "String"
price_tier: ["Budget_Ready", "Business", "Premium_Ultra"]
price_range_rub: [min, max]
source_urls: ["URL1", "URL2"]
hook: "String"
usps: ["String"]
tech_aesthetic_features: ["String"]
cases:
  - title: "String"
    link: "URL"
    result: "String"
date_added: "YYYY-MM-DD"
date_verified: "YYYY-MM-DD"
status: ["Verified", "Pending", "Outdated"]
tags: ["string"]
note_id: "domain|competitor|service_type|date_verified"
```

### Contract B — `content_core` (priority for new content)

```yaml
id: "string"               # or note_id
type: "market_map|demand_map|catalog|offers_library|..."
domain: "slug-like value"  # e.g. furniture, residential-interiors, interior-commercial
tags: ["string"]
created_at: "YYYY-MM-DD"   # optional but recommended
updated_at: "YYYY-MM-DD"   # optional but recommended
status: "active|draft|deprecated|..."  # optional
```

### Contract C — `doc_core` (system docs)

```yaml
doc_id: "string"
doc_type: "string"
date_added: "YYYY-MM-DD"
tags: ["string"]
date_verified: "YYYY-MM-DD"   # optional but recommended
status: "active|complete|archived|..." # optional
```

## Naming

- File naming: `YYYY-MM-DD_CompetitorName_Service.md`
- Deterministic `note_id`: `domain|competitor|service_type|date_verified`

## Source Quality

- Allowed classes: official sites, verified portfolios, rate cards, anonymized contracts, reputable aggregators.
- Max source age for active pricing: 30 days.
- Every claim requires URL + access date + snapshot SHA256.

## Price Validation

- Normalize to `RUB/m2` or `package_rub`.
- If hidden price: derive from verified budgets + tier mapping and mark with `est.` in note body.
- Cross-check with >=2 sources for `Verified`.
- If spread >20%: set `draft_conflict` in tier rules and log in [[conflicts]].

## Freshness Rules

- >30 days since `date_verified`: re-verify queue.
- >180 days since `date_verified`: set `Outdated`.

## Automated Checks

Run:

```bash
python3 scripts/materialize_tier_rules.py --check
python3 scripts/validate_kb.py
```
