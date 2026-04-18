---
doc_id: update_protocol
doc_type: operations
status: active
date_added: 2026-04-17
date_verified: 2026-04-17
tags: [operations, cadence]
---

# Update Protocol

## Cadence

- Weekly batch update (mandatory).
- Event-driven update when new pricing/cases appear.

## Weekly Runbook

1. Collect new sources for top-30 competitors.
2. Capture snapshots and SHA256.
3. Update domain notes via templates.
4. Update tier evidence and exceptions if needed.
5. Run validation scripts.
6. Review conflicts and freshness queue.

## Event-Driven Triggers

- Published updated price cards.
- New service package launch.
- Significant portfolio case with explicit budgets.
- New material/tech trend with commercial impact.

## Exit Criteria per Cycle

- >=90% active pricing verified within 30 days.
- All `draft_conflict` entries have owner and ETA.
- No broken links in MOC paths.
