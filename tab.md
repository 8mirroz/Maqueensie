````markdown
# /10_Guides/tier_rules.md
---
doc_id: tier_rules_master
doc_type: canonical_rules_table
version: 1.0.0
currency: RUB
geo_scope_default:
  - Moscow
  - Moscow Oblast
metrics_allowed:
  - rub_m2
  - package_rub
domains:
  - Architecture
  - Interior
  - Renovation
  - Decor
  - Furniture
  - RealEstate
validation_profile: tier_rules_v1
last_updated: 2026-04-17
owner: market-intelligence
status: active
---

# tier_rules_master

## Validation Logic

- budget_max_rub < business_min_rub <= business_max_rub < premium_min_rub
- Tier ranges must not overlap
- `status=active` only if `source_count_verified >= 2`
- `metric_type=package_rub` => `area_band_m2_min/max` empty
- `effective_to >= effective_from`
- `rule_id` unique
- Any threshold change => new row with new `rule_id`
- If sources <2 => `draft`
- If sources conflict >20% => `draft_conflict`
- If stale beyond review_cycle_days => mark `review_due`

| rule_id | domain | subdomain_scope | service_type_scope | metric_type | geo_scope | object_segment | area_band_m2_min | area_band_m2_max | budget_min_rub | budget_max_rub | business_min_rub | business_max_rub | premium_min_rub | premium_max_rub | sample_size_n | source_count_verified | source_urls | source_access_dates | snapshot_hashes | effective_from | effective_to | review_cycle_days | status | owner | reviewer | notes |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---:|---|---|---|---|
| TR-ARCH-RM2-001 | Architecture | residential | concept_design | rub_m2 | Moscow | comfort | 80 | 250 | 1500 | 3500 | 3501 | 7000 | 7001 | 15000 | 18 | 2 | https://a.ru;https://b.ru | 2026-04-10;2026-04-11 | sha256:a1;sha256:b1 | 2026-04-17 | 2026-12-31 | 90 | active | research_team | lead_analyst | verified sample |
| TR-ARCH-PKG-001 | Architecture | residential | full_project | package_rub | Moscow | comfort |  |  | 120000 | 300000 | 300001 | 700000 | 700001 | 2500000 | 9 | 1 | https://c.ru | 2026-04-10 | sha256:c1 | 2026-04-17 | 2026-12-31 | 60 | draft | research_team | lead_analyst | insufficient evidence |
| TR-INT-RM2-001 | Interior | apartment | design_only | rub_m2 | Moscow | comfort | 40 | 180 | 2000 | 5000 | 5001 | 9000 | 9001 | 18000 | 15 | 1 | https://d.ru | 2026-04-10 | sha256:d1 | 2026-04-17 | 2026-12-31 | 60 | draft | research_team | lead_analyst | pending second source |
| TR-INT-PKG-001 | Interior | apartment | turnkey_design | package_rub | Moscow | comfort |  |  | 150000 | 400000 | 400001 | 900000 | 900001 | 3000000 | 7 | 1 | https://e.ru | 2026-04-10 | sha256:e1 | 2026-04-17 | 2026-12-31 | 60 | draft | research_team | lead_analyst | insufficient evidence |
| TR-REN-RM2-001 | Renovation | apartment | cosmetic | rub_m2 | Moscow Oblast | standard | 30 | 150 | 7000 | 14000 | 14001 | 26000 | 26001 | 50000 | 21 | 1 | https://f.ru | 2026-04-10 | sha256:f1 | 2026-04-17 | 2026-12-31 | 45 | draft | research_team | lead_analyst | pending validation |
| TR-REN-PKG-001 | Renovation | apartment | turnkey | package_rub | Moscow | comfort |  |  | 350000 | 900000 | 900001 | 2500000 | 2500001 | 7000000 | 12 | 1 | https://g.ru | 2026-04-10 | sha256:g1 | 2026-04-17 | 2026-12-31 | 45 | draft | research_team | lead_analyst | insufficient evidence |
| TR-DEC-RM2-001 | Decor | apartment | styling | rub_m2 | Moscow | comfort | 40 | 220 | 1200 | 3000 | 3001 | 7000 | 7001 | 14000 | 8 | 1 | https://h.ru | 2026-04-10 | sha256:h1 | 2026-04-17 | 2026-12-31 | 90 | draft | research_team | lead_analyst | early baseline |
| TR-DEC-PKG-001 | Decor | apartment | package_styling | package_rub | Moscow | comfort |  |  | 80000 | 220000 | 220001 | 600000 | 600001 | 1800000 | 6 | 1 | https://i.ru | 2026-04-10 | sha256:i1 | 2026-04-17 | 2026-12-31 | 90 | draft | research_team | lead_analyst | insufficient evidence |
| TR-FUR-RM2-001 | Furniture | custom | built_in | rub_m2 | Moscow | comfort | 10 | 80 | 9000 | 22000 | 22001 | 50000 | 50001 | 110000 | 10 | 1 | https://j.ru | 2026-04-10 | sha256:j1 | 2026-04-17 | 2026-12-31 | 60 | draft | research_team | lead_analyst | benchmark row |
| TR-FUR-PKG-001 | Furniture | custom | kitchen_set | package_rub | Moscow | comfort |  |  | 180000 | 500000 | 500001 | 1500000 | 1500001 | 5000000 | 14 | 1 | https://k.ru | 2026-04-10 | sha256:k1 | 2026-04-17 | 2026-12-31 | 60 | draft | research_team | lead_analyst | pending source |
| TR-RE-RM2-001 | RealEstate | new_build | fitout_ready | rub_m2 | Moscow | business | 25 | 200 | 220000 | 350000 | 350001 | 550000 | 550001 | 1200000 | 25 | 1 | https://l.ru | 2026-04-10 | sha256:l1 | 2026-04-17 | 2026-12-31 | 30 | draft | research_team | lead_analyst | market snapshot |
| TR-RE-PKG-001 | RealEstate | new_build | unit_package | package_rub | Moscow | business |  |  | 9000000 | 18000000 | 18000001 | 42000000 | 42000001 | 150000000 | 20 | 1 | https://m.ru | 2026-04-10 | sha256:m1 | 2026-04-17 | 2026-12-31 | 30 | draft | research_team | lead_analyst | insufficient evidence |

## Dataview Query

```dataview
TABLE domain, metric_type, budget_min_rub, budget_max_rub, business_min_rub, business_max_rub, premium_min_rub, premium_max_rub, effective_from, effective_to, source_count_verified
FROM "10_Guides"
WHERE doc_id = "tier_rules_master"
FLATTEN rows AS row
WHERE row.status = "active"
SORT row.domain ASC
````

## QA Checks

* [x] All required columns present
* [x] 6 domains included
* [x] At least one active rule
* [x] Draft fallback used where sources <2
* [x] Active rows contain non-empty required fields
* [x] Tier ranges non-overlapping in examples

````

```markdown
# /10_Guides/tier_rules_exceptions.md
---
doc_id: tier_rules_exceptions
version: 1.0.0
status: active
---

# tier_rules_exceptions

| exception_id | rule_id | competitor | service_type | metric_type | override_budget_max_rub | override_business_min_rub | override_business_max_rub | override_premium_min_rub | reason | source_urls | source_access_dates | snapshot_hashes | status | approved_by | date_added | date_verified |
|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|---|---|---|---|
| EX-001 | TR-INT-RM2-001 | StudioX | design_only | rub_m2 | 6500 | 6501 | 11000 | 11001 | niche premium branding uplift | https://n.ru;https://o.ru | 2026-04-12;2026-04-12 | sha256:n1;sha256:o1 | active | pricing_board | 2026-04-17 | 2026-04-17 |

## QA Checks
- [x] rule_id linked
- [x] Example override present
- [x] Sources included
````

```markdown
# /10_Guides/tier_rules_changelog.md
---
doc_id: tier_rules_changelog
version: 1.0.0
status: active
---

# tier_rules_changelog

| change_id | timestamp | actor | action | target_rule_id | old_values_ref | new_values_ref | reason | approval_ref |
|---|---|---|---|---|---|---|---|---|
| CH-001 | 2026-04-17T12:00:00+03:00 | lead_analyst | create | TR-ARCH-RM2-001 | null | TR-ARCH-RM2-001 | initial verified baseline | APR-001 |
| CH-002 | 2026-04-17T12:30:00+03:00 | lead_analyst | flag_conflict | TR-REN-RM2-001 | TR-REN-RM2-001 | TR-REN-RM2-001 | source spread exceeded 20% | APR-002 |

## QA Checks
- [x] Audit trail exists
- [x] Conflict example logged
```

```markdown
# /10_Guides/tier_rules_evidence.md
---
doc_id: tier_rules_evidence
version: 1.0.0
status: active
---

# tier_rules_evidence

| evidence_id | rule_id | source_url | source_type | access_date | snapshot_path | snapshot_sha256 | claim_excerpt | claim_type | verified_by |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | TR-ARCH-RM2-001 | https://a.ru | website | 2026-04-10 | /snapshots/a.html | sha256:a1 | concept design pricing from 1500/m2 | price_claim | qa_team |
| EV-002 | TR-ARCH-RM2-001 | https://b.ru | marketplace | 2026-04-11 | /snapshots/b.html | sha256:b1 | premium projects above 7000/m2 | price_claim | qa_team |
| EV-003 | TR-INT-RM2-001 | https://d.ru | website | 2026-04-10 | /snapshots/d.html | sha256:d1 | apartment design baseline prices | benchmark | qa_team |

## QA Checks
- [x] Evidence linked to rules
- [x] URL + date + SHA256 present
- [x] Verified_by populated
```
