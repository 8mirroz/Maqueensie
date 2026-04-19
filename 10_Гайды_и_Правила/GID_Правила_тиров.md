---
doc_id: tier_rules_master
doc_type: canonical_rules_table
version: 1.0.0
currency: RUB
geo_scope_default: [Moscow, Moscow_Oblast]
metrics_allowed: [rub_m2, package_rub]
status: active
source_file: obsidian_tier_rules_spec.xlsx
last_materialized: 2026-04-19

title: "Правила тиров"---

# tier_rules_master

## Validation Logic

- `economy_max_rub < comfort_min_rub <= comfort_max_rub < business_min_rub <= business_max_rub < premium_min_rub`
- Tier ranges must not overlap
- `status=active` only if `source_count_verified >= 2`
- `metric_type=package_rub` requires empty `area_band_m2_min/max`
- `effective_to` must be empty or `>= effective_from`
- Any threshold update creates a new `rule_id`
| rule_id | domain | subdomain_scope | service_type_scope | metric_type | geo_scope | object_segment | area_band_m2_min | area_band_m2_max | economy_min_rub | economy_max_rub | comfort_min_rub | comfort_max_rub | business_min_rub | business_max_rub | premium_min_rub | premium_max_rub | sample_size_n | source_count_verified | source_urls | source_access_dates | snapshot_hashes | effective_from | effective_to | review_cycle_days | status | owner | reviewer | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TR-ARCH-RUBM2-MOW-MO-0001-V1 | Architecture | private_houses | concept_design | rub_m2 | Moscow+MoscowOblast | mid_to_high | 150 | 350 | 2500 | 4500 |  |  | 4501 | 9000 | 9001 | 18000 | 18 | 2 | https://example.com/arch-source-1; https://example.com/arch-source-2 | 2026-04-17; 2026-04-17 | sha256:1111111111111111111111111111111111111111111111111111111111111111; sha256:2222222222222222222222222222222222222222222222222222222222222222 | 2026-04-17 |  | 30 | active | market-intel-bot | lead-data-architect | Validated active example with >=2 verified sources |
| TR-INT-PKG-MOW-MO-0001-V1 | Interior | apartments | full_design_package | package_rub | Moscow+MoscowOblast | business |  |  | 1000 | 3000 | 3001 | 5000 | 5001 | 8000 | 8001 | 15000 | 24 | 2 | https://example.com/interior-package-1; https://example.com/interior-package-2 | 2026-04-17; 2026-04-17 | sha256:3333333333333333333333333333333333333333333333333333333333333333; sha256:4444444444444444444444444444444444444444444444444444444444444444 | 2026-04-17 |  | 30 | active | market-intel-bot | lead-data-architect | Validated active package rule with >=2 verified sources |
| TR-ARCH-RUBM2-MOWMO-D001-V1 | Architecture | private_houses | concept_design | rub_m2 | Moscow+MoscowOblast | all | 50 | 250 | 1000 | 2000 |  |  | 2001 | 3500 | 3501 | 6000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence |
| TR-ARCH-PKG-MOWMO-D001-V1 | Architecture | private_houses | concept_design_package | package_rub | Moscow+MoscowOblast | all |  |  | 50000 | 120000 |  |  | 120001 | 300000 | 300001 | 900000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence |
| TR-INTE-RUBM2-MOWMO-D002-V1 | Interior | apartments | full_design | rub_m2 | Moscow+MoscowOblast | all | 50 | 250 | 1000 | 3000 | 3001 | 5000 | 5001 | 8000 | 8001 | 15000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence |
| TR-INTE-PKG-MOWMO-D002-V1 | Interior | apartments | full_design_package | package_rub | Moscow+MoscowOblast | all |  |  | 1000 | 3000 | 3001 | 5000 | 5001 | 8000 | 8001 | 15000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence |
| TR-RENO-RUBM2-MOWMO-D003-V1 | Renovation | apartments | turnkey_renovation | rub_m2 | Moscow+MoscowOblast | all | 50 | 250 | 12000 | 20000 | 20001 | 35000 | 35001 | 65000 | 70000 | 150000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence |
| TR-RENO-PKG-MOWMO-D003-V1 | Renovation | apartments | turnkey_renovation_package | package_rub | Moscow+MoscowOblast | all |  |  | 12000 | 20000 | 20001 | 35000 | 35001 | 65000 | 70000 | 150000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence |
| TR-DECO-RUBM2-MOWMO-D004-V1 | Decor | residential | decor_styling | rub_m2 | Moscow+MoscowOblast | all | 50 | 250 | 4000 | 8000 |  |  | 8001 | 14000 | 14001 | 24000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence |
| TR-DECO-PKG-MOWMO-D004-V1 | Decor | residential | decor_styling_package | package_rub | Moscow+MoscowOblast | all |  |  | 200000 | 480000 |  |  | 480001 | 1200000 | 1200001 | 3600000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence |
| TR-FURN-RUBM2-MOWMO-D005-V1 | Furniture | custom_furniture | kitchen_cabinetry | rub_m2 | Moscow+MoscowOblast | all | 50 | 250 | 5000 | 10000 |  |  | 10001 | 17500 | 17501 | 30000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence |
| TR-FURN-PKG-MOWMO-D005-V1 | Furniture | custom_furniture | kitchen_cabinetry_package | package_rub | Moscow+MoscowOblast | all |  |  | 250000 | 600000 |  |  | 600001 | 1500000 | 1500001 | 4500000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence |
| TR-REAL-RUBM2-MOWMO-D006-V1 | RealEstate | new_build | brokerage_selection | rub_m2 | Moscow+MoscowOblast | all | 50 | 250 | 6000 | 12000 |  |  | 12001 | 21000 | 21001 | 36000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence |
| TR-REAL-PKG-MOWMO-D006-V1 | RealEstate | new_build | brokerage_selection_package | package_rub | Moscow+MoscowOblast | all |  |  | 300000 | 720000 |  |  | 720001 | 1800000 | 1800001 | 5400000 | 0 | 0 |  |  |  | 2026-04-17 |  | 30 | draft | market-intel-bot |  | insufficient evidence; package_rub not primary market metric; retained for comparable service bundles only |

## QA Checks

- [x] Canonical source is `obsidian_tier_rules_spec.xlsx`
- [x] Multiline list fields normalized with `;` separator
- [x] Date fields normalized to `YYYY-MM-DD` where applicable
- [x] Status values constrained by whitelist
