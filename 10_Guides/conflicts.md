---
doc_id: conflicts_log
doc_type: registry
status: active
date_added: 2026-04-17
date_verified: 2026-04-17
tags: [conflicts, pricing, validation]
---

# Conflicts Log

| conflict_id | date | domain | competitor | service_type | conflicting_sources | spread_pct | current_status | owner | resolution_path | eta |
|---|---|---|---|---|---|---:|---|---|---|---|
| CF-2026-001 | 2026-04-17 | Renovation | TBD | turnkey_renovation | source_A vs source_B | 22.4 | open | lead_analyst | gather 3rd source, reclassify tier | 2026-04-24 |

## Resolution Rules

- If spread <=20%: median accepted with note.
- If spread >20%: keep `draft_conflict` until resolved.
- Every resolution updates [[10_Guides/tier_rules_changelog]].
