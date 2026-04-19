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

STRICT_REQUIRED_YAML_KEYS = {
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

CONTENT_REQUIRED_YAML_KEYS = {
    "type",
    "domain",
    "tags",
}

DOC_REQUIRED_YAML_KEYS = {
    "doc_id",
    "doc_type",
    "date_added",
    "tags",
}

STRICT_DOMAIN_ENUM = {
    "Architecture",
    "Interior",
    "Renovation",
    "Decor",
    "Furniture",
    "RealEstate",
}

TIER_ENUM = {"Economy", "Comfort", "Business", "Premium", "Budget_Ready", "Premium_Ultra"}
STATUS_ENUM = {
    "Verified",
    "Pending",
    "Outdated",
    "draft",
    "active",
    "draft_conflict",
    "deprecated",
    "wip",
    "complete",
    "candidate",
    "archived",
}

STRICT_DOMAIN_ENUM = {
    "Architecture",
    "Interior",
    "Renovation",
    "Decor",
    "Furniture",
    "RealEstate",
}

TIER_ENUM = {"Economy", "Comfort", "Business", "Premium", "Budget_Ready", "Premium_Ultra"}

DOMAIN_SLUG_RE = re.compile(r"^[a-z0-9_-]+$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def fail(msg: str, errors: List[str]) -> None:
    errors.append(msg)


def warn(msg: str, warnings: List[str]) -> None:
    warnings.append(msg)


def scalar(val: any) -> str:
    if isinstance(val, list) and val:
        return str(val[0])
    return str(val or "")


def parse_frontmatter(text: str) -> Tuple[Dict, bool]:
    if not text.startswith("---"):
        return {}, False
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, False
    import yaml

    try:
        data = yaml.safe_load(parts[1])
        return data or {}, True
    except Exception:
        return {}, False


def is_doc_contract_note(fm: Dict) -> bool:
    return "doc_id" in fm


def is_legacy_contract_note(path: Path, fm: Dict) -> bool:
    return "07_Competitors" in str(path) or "competitor" in fm


def parse_markdown_table(path: Path, row_prefix: str) -> List[Dict]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    header_idx = -1
    for i, line in enumerate(lines):
        if "|" in line and "rule_id" in line.lower():
            header_idx = i
            break
    if header_idx == -1:
        return []

    headers = [h.strip().lower() for h in lines[header_idx].split("|")][1:-1]
    out = []
    for line in lines[header_idx + 2 :]:
        if not line.strip() or "|" not in line:
            continue
        cells = [c.strip() for c in line.split("|")][1:-1]
        if not cells or not (cells[0] or "").startswith(row_prefix):
            continue
        row = dict(zip(headers, cells))
        out.append(row)
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
        for path in sorted((ROOT / folder).rglob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            note_count += 1
            text = path.read_text(encoding="utf-8")
            fm, ok = parse_frontmatter(text)
            if not ok:
                fail(f"missing/invalid frontmatter: {path.relative_to(ROOT)}", errors)
                continue

            keys = set(fm.keys())
            if is_doc_contract_note(fm):
                missing = DOC_REQUIRED_YAML_KEYS - keys
                if missing:
                    fail(f"missing doc YAML keys in {path.relative_to(ROOT)}: {sorted(missing)}", errors)
            elif is_legacy_contract_note(path, fm):
                missing = STRICT_REQUIRED_YAML_KEYS - keys
                if missing:
                    fail(f"missing YAML keys in {path.relative_to(ROOT)}: {sorted(missing)}", errors)

                domain_raw = fm.get("domain", "")
                if not any(d in domain_raw for d in STRICT_DOMAIN_ENUM):
                    fail(f"invalid domain enum in {path.relative_to(ROOT)}", errors)

                tier_raw = fm.get("price_tier", "")
                if not any(t in tier_raw for t in TIER_ENUM):
                    fail(f"invalid price_tier enum in {path.relative_to(ROOT)}", errors)
            else:
                missing = CONTENT_REQUIRED_YAML_KEYS - keys
                if missing:
                    fail(f"missing content YAML keys in {path.relative_to(ROOT)}: {sorted(missing)}", errors)
                if "id" not in keys and "note_id" not in keys:
                    fail(f"missing id/note_id in {path.relative_to(ROOT)}", errors)

                domain_raw = scalar(fm.get("domain", ""))
                if domain_raw and not DOMAIN_SLUG_RE.match(domain_raw):
                    fail(f"invalid content domain format in {path.relative_to(ROOT)}", errors)

            status_raw = fm.get("status", "")
            if status_raw and not any(s in status_raw for s in STATUS_ENUM):
                fail(f"invalid status enum in {path.relative_to(ROOT)}", errors)

            for date_field in ("created", "created_at", "updated_at", "date_added", "date_verified"):
                raw = scalar(fm.get(date_field, ""))
                if raw and not ISO_DATE_RE.match(raw):
                    fail(f"invalid {date_field} format in {path.relative_to(ROOT)}: {raw}", errors)

            if is_legacy_contract_note(path, fm):
                raw_verified = scalar(fm.get("date_verified", ""))
                if ISO_DATE_RE.match(raw_verified):
                    d = dt.date.fromisoformat(raw_verified)
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
    expected = STRICT_DOMAIN_ENUM
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

        emin = num("economy_min_rub")
        emax = num("economy_max_rub")
        commin = num("comfort_min_rub")
        commax = num("comfort_max_rub")
        bmin = num("business_min_rub")
        bmax = num("business_max_rub")
        pmin = num("premium_min_rub")
        pmax = num("premium_max_rub")

        if None not in (emin, emax, bmin, bmax, pmin):
            upper_p = pmax if pmax is not None else pmin
            # Order: Economy -> Comfort (optional) -> Business -> Premium
            checks = [emin <= emax]
            if commin is not None and commax is not None:
                checks.append(emax < commin <= commax < bmin)
            else:
                checks.append(emax < bmin)
            checks.append(bmin <= bmax < pmin <= upper_p)
            
            if not all(checks):
                print(f"DEBUG: {rid} checks failed: {checks} (values: emin={emin}, emax={emax}, commin={commin}, commax={commax}, bmin={bmin}, bmax={bmax}, pmin={pmin}, pmax={pmax})")
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
    optional = ROOT / "08_Pricing_Tables/04_Repair_Price_Matrix.md"
    if optional.exists():
        files.append(optional)
    for f in files:
        if not f.exists():
            continue
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
    import sys
    sys.exit(main())
