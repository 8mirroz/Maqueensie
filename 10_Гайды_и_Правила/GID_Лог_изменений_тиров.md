---
doc_id: tier_rules_changelog
version: 1.0.0
status: active
source_file: obsidian_tier_rules_spec.xlsx
last_materialized: 2026-04-19

title: "Лог изменений тиров"---

# tier_rules_changelog
| change_id | timestamp | actor | action | target_rule_id | old_values_ref | new_values_ref | reason | approval_ref |
|---|---|---|---|---|---|---|---|---|
| CHG-0001 | 2026-04-17T12:00:00 | lead-data-architect | create_active_rule | TR-ARCH-RUBM2-MOW-MO-0001-V1 | N/A | tier_rules_master!A2:AA2 | Initial active publication after 2-source verification | APP-0001 |
| CHG-0002 | 2026-04-17T12:15:00 | market-intel-bot | log_conflict | TR-REAL-PKG-MOWMO-D006-V1 | tier_rules_master!A14:AA14 | tier_rules_master!A14:AA14 | Example failsafe note: if future sources diverge >20%, set draft_conflict and trigger review | APP-0002 |

## QA Checks

- [x] Canonical source is `obsidian_tier_rules_spec.xlsx`
- [x] Multiline list fields normalized with `;` separator
- [x] Date fields normalized to `YYYY-MM-DD` where applicable
- [x] Status values constrained by whitelist
