# Maqueensie Knowledge Base

Production-ready Obsidian + NotebookLM knowledge base for Moscow/MO market intelligence.

## Vault Tree

```text
.
├── 00_MOC
│   ├── 00_Master_MOC.md
│   ├── 01_Architecture_MOC.md
│   ├── 02_Interior_MOC.md
│   ├── 03_Renovation_MOC.md
│   ├── 04_Decor_MOC.md
│   ├── 05_Furniture_MOC.md
│   ├── 06_RealEstate_MOC.md
│   ├── 07_Competitors_MOC.md
│   ├── 08_Pricing_Tables_MOC.md
│   └── 10_Guides_MOC.md
├── 01_Architecture
├── 02_Interior
├── 03_Renovation
├── 04_Decor
├── 05_Furniture
├── 06_RealEstate
├── 07_Competitors
├── 08_Pricing_Tables
│   ├── 01_Price_Matrix.md
│   ├── 02_Competitor_Comparison_Dashboard.md
│   └── 03_Trend_Tracker.md
├── 09_Templates
│   ├── Competitor_Profile.md
│   ├── Service_Analysis.md
│   └── Pricing_Tracker.md
├── 10_Guides
│   ├── conflicts.md
│   ├── nblm_sync_protocol.md
│   ├── tier_rules.md
│   ├── tier_rules_changelog.md
│   ├── tier_rules_evidence.md
│   ├── tier_rules_exceptions.md
│   ├── update_protocol.md
│   └── validation_rules.md
├── .githooks
│   └── pre-commit
├── .obsidian
│   ├── app.json
│   ├── community-plugins.json
│   ├── core-plugins.json
│   └── workspace.json
├── config
│   └── integrations
│       ├── notebooklm.yaml
│       └── obsidian.yaml
├── scripts
│   ├── automate_notebooklm.py
│   ├── check_integrations.py
│   ├── export_nblm_bundles.py
│   ├── materialize_tier_rules.py
│   ├── setup_notebooklm_auth.py
│   ├── setup_hooks.sh
│   └── validate_kb.py
├── .env.example
├── obsidian_tier_rules_spec.xlsx
└── tab.md
```

## Commands

```bash
python3 scripts/materialize_tier_rules.py
python3 scripts/materialize_tier_rules.py --check
python3 scripts/validate_kb.py
python3 scripts/check_integrations.py
python3 scripts/export_nblm_bundles.py
python3 scripts/setup_notebooklm_auth.py   # one-time browser auth bootstrap
python3 scripts/automate_notebooklm.py     # optional API-based flow
```

## Git Hooks

```bash
git init                    # if repo is not initialized yet
./scripts/setup_hooks.sh
```

## Notes

- Canonical source of tier rules: `obsidian_tier_rules_spec.xlsx`.
- `python3 scripts/materialize_tier_rules.py --check` ignores volatile `last_materialized` date field when comparing generated guides.
- `python3 scripts/check_integrations.py` now includes Python script syntax smoke-check (`py_compile`).
