---
doc_id: validation_rules
doc_type: policy
status: active
date_added: 2026-04-17
date_verified: 2026-04-17
tags: [validation, policy]
---

# Validation Rules

## Required YAML Contract (all working notes in `01_*`..`07_*`)

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
- If spread >20%: set `draft_conflict` in tier rules and log in [[10_Guides/conflicts]].

## Freshness Rules

- >30 days since `date_verified`: re-verify queue.
- >180 days since `date_verified`: set `Outdated`.

## Automated Checks

Run:

```bash
python3 scripts/materialize_tier_rules.py --check
python3 scripts/validate_kb.py
```
