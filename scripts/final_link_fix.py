#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAPPING = {
    "validation_rules": "GID_Правила_валидации",
    "01_Price_Matrix": "PRC_Матрица_цен_общая",
    "02_Competitor_Comparison_Dashboard": "PRC_Дашборд_сравнения_конкурентов",
    "03_Trend_Tracker": "PRC_Трекер_трендов",
    "04_Repair_Price_Matrix": "PRC_Матрица_цен_ремонт",
    "REPOSITORY_DEVELOPMENT_PLAN": "DEV_План_развития_репозитория",
    "Furniture_MOC": "MOC_Мебель",
    "NAV_Карта_Раздела": "NAV_Карта_раздела",
    "RYN_Обзор_рынка": "RYN_Обзор_рынка_ремонта",
    "repair_works_registry_master": "PRC_Мастер_реестр_ремонтных_работ",
}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)([\]|#])")

def fix_links(text: str) -> str:
    def replacer(match):
        target = match.group(1).strip()
        sep = match.group(2)
        if target in MAPPING:
            return f"[[{MAPPING[target]}{sep}"
        return match.group(0)
    
    return WIKILINK_RE.sub(replacer, text)

def main():
    count = 0
    for path in ROOT.rglob("*.md"):
        if ".obsidian" in str(path) or "scripts/" in str(path):
            continue
        
        orig_text = path.read_text(encoding="utf-8")
        new_text = fix_links(orig_text)
        
        if orig_text != new_text:
            path.write_text(new_text, encoding="utf-8")
            print(f"Fixed links in: {path.relative_to(ROOT)}")
            count += 1
            
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    main()
