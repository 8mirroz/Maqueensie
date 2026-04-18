#!/usr/bin/env python3
"""Export domain markdown bundles for NotebookLM ingestion.

- Flattens notes from 01_*..06_* folders.
- Strips YAML frontmatter.
- Keeps citation lines in note body.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "exports" / "nblm"
DOMAINS = [
    "01_Architecture",
    "02_Interior",
    "03_Renovation",
    "04_Decor",
    "05_Furniture",
    "06_RealEstate",
]

FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def main() -> int:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    for domain in DOMAINS:
        folder = ROOT / domain
        notes = sorted(
            p
            for p in folder.glob("*.md")
            if p.is_file() and p.name.lower() != "readme.md"
        )

        out_lines = [f"# {domain} Bundle", ""]
        for note in notes:
            body = strip_frontmatter(note.read_text(encoding="utf-8")).strip()
            if not body:
                continue
            out_lines.append(f"## {note.stem}")
            out_lines.append("")
            out_lines.append(body)
            out_lines.append("")

        out_path = EXPORT_DIR / f"{domain}_bundle.md"
        out_path.write_text("\n".join(out_lines).rstrip() + "\n", encoding="utf-8")
        print(f"wrote {out_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
