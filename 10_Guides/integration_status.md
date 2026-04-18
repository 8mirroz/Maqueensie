---
doc_id: integration_status
doc_type: operational_status
status: active
date_added: 2026-04-17
date_verified: 2026-04-17
tags: [integration, status, obsidian, notebooklm]
---

# Integration Status

## Obsidian

- State: `configured`.
- Config present: `.obsidian/app.json`, `.obsidian/core-plugins.json`, `.obsidian/community-plugins.json`.
- Required community plugins: `dataview`, `templater-obsidian`.
- Dashboards ready: `08_Pricing_Tables/*`.

## NotebookLM

- State: `configured_manual`.
- Integration mode: manual upload from domain bundles (`exports/nblm/*_bundle.md`).
- Protocol: [[10_Guides/nblm_sync_protocol]].
- API connection in repo: not configured.

## Verification

Run:

```bash
python3 scripts/check_integrations.py
```
