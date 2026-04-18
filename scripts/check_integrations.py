#!/usr/bin/env python3
"""Check integration readiness for Obsidian and NotebookLM in this repo."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ok(msg: str) -> None:
    print(f"OK: {msg}")


def warn(msg: str) -> None:
    print(f"WARN: {msg}")


def err(msg: str) -> None:
    print(f"ERROR: {msg}")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_obsidian() -> int:
    failures = 0
    obs = ROOT / ".obsidian"
    if not obs.exists():
        err(".obsidian folder is missing")
        return 1

    app = obs / "app.json"
    core = obs / "core-plugins.json"
    community = obs / "community-plugins.json"

    for p in (app, core, community):
        if not p.exists():
            err(f"missing Obsidian config file: {p.relative_to(ROOT)}")
            failures += 1

    if failures:
        return failures

    community_plugins = set(read_json(community))
    if "dataview" not in community_plugins:
        err("dataview plugin is not listed in community-plugins.json")
        failures += 1
    else:
        ok("dataview plugin configured")

    if "templater-obsidian" not in community_plugins:
        warn("templater-obsidian not configured")
    else:
        ok("templater plugin configured")

    dashboards = [
        ROOT / "08_Pricing_Tables/01_Price_Matrix.md",
        ROOT / "08_Pricing_Tables/02_Competitor_Comparison_Dashboard.md",
        ROOT / "08_Pricing_Tables/03_Trend_Tracker.md",
    ]
    for d in dashboards:
        if d.exists():
            ok(f"dashboard present: {d.relative_to(ROOT)}")
        else:
            err(f"dashboard missing: {d.relative_to(ROOT)}")
            failures += 1

    return failures


def check_notebooklm() -> int:
    failures = 0
    protocol = ROOT / "10_Guides/nblm_sync_protocol.md"
    export_script = ROOT / "scripts/export_nblm_bundles.py"
    automate_script = ROOT / "scripts/automate_notebooklm.py"
    auth_script = ROOT / "scripts/setup_notebooklm_auth.py"
    out = ROOT / "exports/nblm"

    if not protocol.exists():
        err("missing NotebookLM protocol doc")
        failures += 1
    else:
        ok("NotebookLM protocol doc present")

    if not export_script.exists():
        err("missing NotebookLM export script")
        failures += 1
    else:
        ok("NotebookLM export script present")

    if not automate_script.exists():
        err("missing NotebookLM automation script")
        failures += 1
    else:
        ok("NotebookLM automation script present")

    if not auth_script.exists():
        err("missing NotebookLM auth setup script")
        failures += 1
    else:
        ok("NotebookLM auth setup script present")

    expected = [
        "01_Architecture_bundle.md",
        "02_Interior_bundle.md",
        "03_Renovation_bundle.md",
        "04_Decor_bundle.md",
        "05_Furniture_bundle.md",
        "06_RealEstate_bundle.md",
    ]

    if not out.exists():
        warn("NotebookLM bundles folder missing; run export_nblm_bundles.py")
        return failures

    missing = [name for name in expected if not (out / name).exists()]
    if missing:
        warn(f"missing NotebookLM bundles: {', '.join(missing)}")
    else:
        ok("all domain bundles present for NotebookLM upload")

    # Check for authentication
    auth_storage = ROOT / ".auth" / "notebooklm_state.json"
    if auth_storage.exists():
        ok("NotebookLM authentication configured")
    else:
        warn("NotebookLM authentication not configured. Run: python3 scripts/setup_notebooklm_auth.py")

    # Check if notebooklm-py is available
    try:
        import notebooklm
        ok("notebooklm-py library available")
    except ImportError:
        err("notebooklm-py library not available")
        failures += 1

    return failures


def check_python_scripts() -> int:
    failures = 0
    scripts = sorted((ROOT / "scripts").glob("*.py"))
    if not scripts:
        warn("no Python scripts found in scripts/")
        return failures

    cmd = [sys.executable, "-m", "py_compile", *[str(p) for p in scripts]]
    result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if result.returncode != 0:
        err("python script syntax check failed (py_compile)")
        output = (result.stderr or result.stdout).strip()
        if output:
            print(output)
        failures += 1
    else:
        ok(f"python scripts compile: {len(scripts)} files")
    return failures


def main() -> int:
    print("== Obsidian Integration ==")
    f1 = check_obsidian()
    print("\n== NotebookLM Integration ==")
    f2 = check_notebooklm()
    print("\n== Script Health ==")
    f3 = check_python_scripts()

    total = f1 + f2 + f3
    print("\n== Summary ==")
    if total == 0:
        ok("integration baseline ready")
        print("INFO: Obsidian is locally configured; NotebookLM workflow is manual-by-design.")
        return 0

    err(f"integration checks failed: {total} issue(s)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
