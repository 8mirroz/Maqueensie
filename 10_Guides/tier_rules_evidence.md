---
doc_id: tier_rules_evidence
version: 1.0.0
status: active
source_file: obsidian_tier_rules_spec.xlsx
last_materialized: 2026-04-19
---

# tier_rules_evidence
| evidence_id | rule_id | source_url | source_type | access_date | snapshot_path | snapshot_sha256 | claim_excerpt | claim_type | verified_by |
|---|---|---|---|---|---|---|---|---|---|
| EVD-0001 | TR-ARCH-RUBM2-MOW-MO-0001-V1 | https://example.com/arch-source-1 | competitor_site | 2026-04-17 | /snapshots/arch-source-1.html | 1111111111111111111111111111111111111111111111111111111111111111 | Concept design from 2,500 to 4,500 RUB/m² in Moscow region | price_range | analyst_1 |
| EVD-0002 | TR-ARCH-RUBM2-MOW-MO-0001-V1 | https://example.com/arch-source-2 | marketplace | 2026-04-17 | /snapshots/arch-source-2.pdf | 2222222222222222222222222222222222222222222222222222222222222222 | Upper segment starts above 9,000 RUB/m² | tier_threshold | analyst_2 |
| EVD-0003 | TR-INT-PKG-MOW-MO-0001-V1 | https://example.com/interior-package-1 | competitor_site | 2026-04-17 | /snapshots/interior-package-1.html | 3333333333333333333333333333333333333333333333333333333333333333 | Apartment design packages begin near 180,000 RUB | package_floor | analyst_1 |
| EVD-0004 | TR-INT-PKG-MOW-MO-0001-V1 | https://example.com/interior-package-2 | aggregator | 2026-04-17 | /snapshots/interior-package-2.html | 4444444444444444444444444444444444444444444444444444444444444444 | Premium full-design packages exceed 1.2M RUB | package_premium | analyst_2 |

## QA Checks

- [x] Canonical source is `obsidian_tier_rules_spec.xlsx`
- [x] Multiline list fields normalized with `;` separator
- [x] Date fields normalized to `YYYY-MM-DD` where applicable
- [x] Status values constrained by whitelist
