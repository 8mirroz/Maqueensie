# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Type

**Maqueensie** is an Obsidian knowledge base + Python tooling for Moscow/Moscow Oblast market intelligence on interior/design/renovation services. It is not a traditional application codebase — the primary artifact is the vault itself, managed through Python scripts and git hooks.

## Commands

```bash
# Materialize tier rules from XLSX spec to Markdown guides
python3 scripts/materialize_tier_rules.py          # write guides
python3 scripts/materialize_tier_rules.py --check  # dry-run / diff

# Validate knowledge base integrity
python3 scripts/validate_kb.py

# Check integration configs
python3 scripts/check_integrations.py

# Export NotebookLM bundles
python3 scripts/export_nblm_bundles.py

# NotebookLM auth/bootstrap (optional API flow)
python3 scripts/setup_notebooklm_auth.py
python3 scripts/automate_notebooklm.py

# Setup git hooks (run once after clone)
./scripts/setup_hooks.sh
```

## Core Data Model: Tier Rules

The canonical source of truth is `obsidian_tier_rules_spec.xlsx`. All other tier rule files are **materialized** from it by `materialize_tier_rules.py`. Never edit the generated `.md` files directly — edit the XLSX and re-materialize.

The XLSX contains four sheets:
- `tier_rules_master` — primary pricing tier rules
- `tier_rules_exceptions` — override rules for specific contexts
- `tier_rules_changelog` — versioned change history
- `tier_rules_evidence` — source-level evidence linked to rules

Each rule encodes service pricing tiers (budget / business / premium) with constraints:
- `budget_max_rub < business_min_rub <= business_max_rub < premium_min_rub`
- Only `status=active` if `source_count_verified >= 2`
- `metric_type=package_rub` requires empty `area_band_m2_min/max`

## Architecture

```
obsidian_tier_rules_spec.xlsx  →  materialize_tier_rules.py  →  10_Guides/tier_rules*.md
                                                                 ↑
                                              validate_kb.py ← git hook (pre-commit)
```

The vault is organized into MOC (Map of Contents) files that aggregate notes by category. The tier rules guides live under `10_Guides/`.

## Git Hooks

Pre-commit hook (installed via `setup_hooks.sh`) validates:
- Materialized tier rule guides are in sync with XLSX (`materialize_tier_rules.py --check`)
- Vault structure, required files, links, and core rule constraints (`validate_kb.py`)
- Obsidian/NotebookLM integration baseline and Python script syntax health (`check_integrations.py`)

Run `git init` and `./scripts/setup_hooks.sh` on first clone.
