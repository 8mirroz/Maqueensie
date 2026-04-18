---
doc_id: nblm_sync_protocol
doc_type: integration
status: active
date_added: 2026-04-17
date_verified: 2026-04-17
tags: [notebooklm, integration, sync]
---

# Obsidian <-> NotebookLM Sync Protocol

## 1) Export (flatten domain notes)

Run:

```bash
python3 scripts/export_nblm_bundles.py
```

Output:

- `exports/nblm/01_Architecture_bundle.md`
- `exports/nblm/02_Interior_bundle.md`
- `exports/nblm/03_Renovation_bundle.md`
- `exports/nblm/04_Decor_bundle.md`
- `exports/nblm/05_Furniture_bundle.md`
- `exports/nblm/06_RealEstate_bundle.md`

Rules:

- Frontmatter stripped.
- Citations retained in body (`Source Log`, URL lines, snapshot refs).

## 2) Ingest into NotebookLM

1. Create one NotebookLM source per domain bundle.
2. Enable `Cite Sources` toggle = ON.
3. Keep domains separated (no mixed uploads in one source file).

## 3) Synthesis Prompts

### A. Hook + USP extraction

```text
Analyze uploaded domain sources. Extract competitor hooks and USPs with exact citation per claim.
Return: Competitor | Hook (RU) | Hook (EN alias) | USP bullets | Citation IDs.
Exclude any statement without citation.
```

### B. Pricing gap analysis

```text
Using only cited evidence, identify pricing gaps by tier (Budget_Ready, Business, Premium_Ultra).
Return: Domain | Service type | Current tier ranges | Observed gap | Opportunity hypothesis | Citations.
Flag uncertain values as est. and explain why.
```

### C. Tech/aesthetic trend mapping

```text
Map trends for materials, layout innovations, smart integrations, bathroom ergonomics, commercial adaptations.
Return: Trend | Domains affected | Competitors using it | Pricing impact | Evidence citations.
```

## 4) Sync Back to Obsidian

1. Paste synthesis outputs into corresponding MOC note section `NotebookLM Synthesis`.
2. Add backlinks to domain notes and competitor profiles.
3. Add tags: `nblm/synthesis`, `nblm/cited`, plus trend tags where relevant.
4. Append source-cited claims only; uncited lines go to `pending` checklist.
