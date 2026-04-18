---
doc_id: tier_rules_exceptions
version: 1.0.0
status: active
source_file: obsidian_tier_rules_spec.xlsx
last_materialized: 2026-04-17
---

# tier_rules_exceptions
| exception_id | rule_id | competitor | service_type | metric_type | override_budget_max_rub | override_business_min_rub | override_business_max_rub | override_premium_min_rub | reason | source_urls | source_access_dates | snapshot_hashes | status | approved_by | date_added | date_verified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EXC-0001 | TR-ARCH-RUBM2-MOW-MO-0001-V1 | Competitor_A | concept_design | rub_m2 | 4800 | 4801 | 9500 | 9501 | Local premium competitor positions entry threshold ~6.7% above master budget_max; localized override retained with verified evidence | https://example.com/competitor-a-pricing; https://example.com/competitor-a-case-study | 2026-04-17; 2026-04-17 | sha256:5555555555555555555555555555555555555555555555555555555555555555; sha256:6666666666666666666666666666666666666666666666666666666666666666 | active | pricing-committee | 2026-04-17 | 2026-04-17 |

## QA Checks

- [x] Canonical source is `obsidian_tier_rules_spec.xlsx`
- [x] Multiline list fields normalized with `;` separator
- [x] Date fields normalized to `YYYY-MM-DD` where applicable
- [x] Status values constrained by whitelist
