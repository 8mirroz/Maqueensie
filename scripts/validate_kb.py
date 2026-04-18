#!/usr/bin/env python3
"""Validate Obsidian knowledge base structure and core data rules."""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRS = [
    "00_MOC",
    "01_Architecture",
    "02_Interior",
    "03_Renovation",
    "04_Decor",
    "05_Furniture",
    "06_RealEstate",
    "07_Competitors",
    "08_Pricing_Tables",
    "09_Templates",
    "10_Guides",
]

REQUIRED_FILES = [
    ".obsidian/app.json",
    ".obsidian/core-plugins.json",
    ".obsidian/community-plugins.json",
    "config/integrations/obsidian.yaml",
    "config/integrations/notebooklm.yaml",
    "10_Guides/tier_rules.md",
    "10_Guides/tier_rules_exceptions.md",
    "10_Guides/tier_rules_changelog.md",
    "10_Guides/tier_rules_evidence.md",
    "10_Guides/update_protocol.md",
    "10_Guides/validation_rules.md",
    "10_Guides/nblm_sync_protocol.md",
    "10_Guides/integration_status.md",
    "10_Guides/conflicts.md",
    "09_Templates/Competitor_Profile.md",
    "09_Templates/Service_Analysis.md",
    "09_Templates/Pricing_Tracker.md",
    "08_Pricing_Tables/01_Price_Matrix.md",
    "08_Pricing_Tables/02_Competitor_Comparison_Dashboard.md",
    "08_Pricing_Tables/03_Trend_Tracker.md",
    "scripts/check_integrations.py",
]

REQUIRED_YAML_KEYS = {
    "domain",
    "subdomain",
    "competitor",
    "service_type",
    "price_tier",
    "price_range_rub",
    "source_urls",
    "hook",
    "usps",
    "tech_aesthetic_features",
    "cases",
    "date_added",
    "date_verified",
    "status",
    "tags",
    "note_id",
}

DOMAIN_ENUM = {
    "Architecture",
    "Interior",
    "Renovation",
    "Decor",
    "Furniture",
    "RealEstate",
}

TIER_ENUM = {"Budget_Ready", "Business", "Premium_Ultra"}
STATUS_ENUM = {"Verified", "Pending", "Outdated", "draft", "active", "draft_conflict", "deprecated"}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def fail(msg: str, errors: List[str]) -> None:
    errors.append(msg)


def warn(msg: str, warnings: List[str]) -> None:
    warnings.append(msg)


def parse_frontmatter(text: str) -> Tuple[Dict[str, str], bool]:
    if not text.startswith("---\n"):
        return {}, False
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, False
    block = text[4:end]
    data: Dict[str, str] = {}
    for line in block.splitlines():
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data, True


def parse_markdown_table(path: Path, row_prefix: str) -> List[Dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    table_lines = [ln for ln in lines if ln.strip().startswith("|")]
    if len(table_lines) < 3:
        return []

    def split_row(line: str) -> List[str]:
        return [x.strip() for x in line.split("|")[1:-1]]

    headers = split_row(table_lines[0])
    out = []
    for row in table_lines[2:]:
        cells = split_row(row)
        if not cells or not cells[0].startswith(row_prefix):
            continue
        padded = cells + [""] * (len(headers) - len(cells))
        out.append(dict(zip(headers, padded[: len(headers)])))
    return out


def check_structure(errors: List[str]) -> None:
    for d in REQUIRED_DIRS:
        if not (ROOT / d).is_dir():
            fail(f"missing directory: {d}", errors)
    for f in REQUIRED_FILES:
        if not (ROOT / f).is_file():
            fail(f"missing file: {f}", errors)


def check_yaml_notes(errors: List[str], warnings: List[str]) -> None:
    folders = [
        "01_Architecture",
        "02_Interior",
        "03_Renovation",
        "04_Decor",
        "05_Furniture",
        "06_RealEstate",
        "07_Competitors",
    ]
    today = dt.date.today()

    note_count = 0
    for folder in folders:
        for path in sorted((ROOT / folder).glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            note_count += 1
            text = path.read_text(encoding="utf-8")
            fm, ok = parse_frontmatter(text)
            if not ok:
                fail(f"missing/invalid frontmatter: {path.relative_to(ROOT)}", errors)
                continue

            keys = set(fm.keys())
            missing = REQUIRED_YAML_KEYS - keys
            if missing:
                fail(f"missing YAML keys in {path.relative_to(ROOT)}: {sorted(missing)}", errors)

            domain_raw = fm.get("domain", "")
            if not any(d in domain_raw for d in DOMAIN_ENUM):
                fail(f"invalid domain enum in {path.relative_to(ROOT)}", errors)

            tier_raw = fm.get("price_tier", "")
            if not any(t in tier_raw for t in TIER_ENUM):
                fail(f"invalid price_tier enum in {path.relative_to(ROOT)}", errors)

            status_raw = fm.get("status", "")
            if not any(s in status_raw for s in STATUS_ENUM):
                fail(f"invalid status enum in {path.relative_to(ROOT)}", errors)

            dv = re.search(r"date_verified:\s*\"?(\d{4}-\d{2}-\d{2})", text)
            if dv:
                d = dt.date.fromisoformat(dv.group(1))
                age = (today - d).days
                if age > 180 and "Outdated" not in status_raw:
                    fail(f"stale note not marked Outdated: {path.relative_to(ROOT)}", errors)
                elif age > 30:
                    warn(f"re-verify due (>30d): {path.relative_to(ROOT)}", warnings)

    if note_count == 0:
        warn("no working notes found in 01_*..07_* yet", warnings)


def check_tier_rules(errors: List[str]) -> None:
    path = ROOT / "10_Guides/tier_rules.md"
    rows = parse_markdown_table(path, "TR-")
    if not rows:
        fail("tier_rules.md has no TR-* rows", errors)
        return

    domains = {r.get("domain", "") for r in rows}
    expected = DOMAIN_ENUM
    if domains != expected:
        fail(f"tier_rules domains mismatch: expected {sorted(expected)}, got {sorted(domains)}", errors)

    for row in rows:
        rid = row.get("rule_id", "")

        def num(k: str) -> float | None:
            raw = (row.get(k, "") or "").strip()
            if not raw:
                return None
            try:
                return float(raw)
            except ValueError:
                fail(f"non-numeric field {k} in {rid}", errors)
                return None

        bmin = num("budget_min_rub")
        bmax = num("budget_max_rub")
        cmin = num("business_min_rub")
        cmax = num("business_max_rub")
        pmin = num("premium_min_rub")
        pmax = num("premium_max_rub")

        if None not in (bmin, bmax, cmin, cmax, pmin):
            upper_p = pmax if pmax is not None else pmin
            if not (bmin <= bmax < cmin <= cmax < pmin <= upper_p):
                fail(f"tier overlap/order violation in {rid}", errors)

        metric = row.get("metric_type", "")
        if metric == "package_rub":
            if (row.get("area_band_m2_min", "") or "").strip() or (row.get("area_band_m2_max", "") or "").strip():
                fail(f"package_rub must keep area_band empty in {rid}", errors)

        if row.get("status") == "active":
            scv = row.get("source_count_verified", "0")
            try:
                if int(float(scv)) < 2:
                    fail(f"active rule with <2 sources: {rid}", errors)
            except ValueError:
                fail(f"invalid source_count_verified in {rid}", errors)

            for field in ("source_urls", "source_access_dates", "snapshot_hashes"):
                if not (row.get(field, "") or "").strip():
                    fail(f"active rule missing {field}: {rid}", errors)


def check_wikilinks(errors: List[str]) -> None:
    all_md = sorted(ROOT.rglob("*.md"))
    stem_index = {}
    for p in all_md:
        stem_index.setdefault(p.stem, []).append(p)

    for md in all_md:
        text = md.read_text(encoding="utf-8")
        for raw in WIKILINK_RE.findall(text):
            target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            if "/" in target:
                candidate = ROOT / (target if target.endswith(".md") else f"{target}.md")
                if not candidate.exists():
                    fail(f"broken wikilink in {md.relative_to(ROOT)} -> [[{raw}]]", errors)
            else:
                matches = stem_index.get(target, [])
                if not matches:
                    fail(f"broken wikilink in {md.relative_to(ROOT)} -> [[{raw}]]", errors)


def check_dataview_blocks(errors: List[str]) -> None:
    files = [
        ROOT / "08_Pricing_Tables/01_Price_Matrix.md",
        ROOT / "08_Pricing_Tables/02_Competitor_Comparison_Dashboard.md",
        ROOT / "08_Pricing_Tables/03_Trend_Tracker.md",
    ]
    for f in files:
        text = f.read_text(encoding="utf-8")
        if "```dataview" not in text and "```dataviewjs" not in text:
            fail(f"missing dataview block: {f.relative_to(ROOT)}", errors)


def main() -> int:
    errors: List[str] = []
    warnings: List[str] = []

    check_structure(errors)
    check_yaml_notes(errors, warnings)
    check_tier_rules(errors)
    check_wikilinks(errors)
    check_dataview_blocks(errors)

    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    if errors:
        print(f"\nValidation failed with {len(errors)} error(s).")
        return 1

    print("\nValidation passed.")
    if warnings:
        print(f"Warnings: {len(warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
