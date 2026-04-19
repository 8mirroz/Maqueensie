#!/usr/bin/env python3
"""
Compute confidence scores for all competitor records.

Confidence formula:
  score = (source_quality × 0.3) + 
          (recency_factor × 0.25) + 
          (cross_validation × 0.25) + 
          (data_completeness × 0.2)

Usage:
  python scripts/analytics/compute_confidence.py [--update-frontmatter]
"""

from __future__ import annotations

import re
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
COMPETITORS_DIR = ROOT / "07_Competitors"
VERIFIED_DIR = COMPETITORS_DIR / "verified"

# Source quality weights
SOURCE_QUALITY_WEIGHTS = {
    "official_site": 1.0,
    "verified_portfolio": 0.9,
    "rate_card": 0.85,
    "reputable_aggregator": 0.7,
    "anonymized_contract": 0.6,
    "forum_social": 0.3,
    "unknown": 0.5,
}


def extract_frontmatter(text: str) -> Dict[str, str]:
    """Extract frontmatter from markdown text."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    block = text[4:end]
    data: Dict[str, str] = {}
    for line in block.splitlines():
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def classify_source_quality(source_urls: List[str]) -> float:
    """Classify source quality based on URL patterns."""
    if not source_urls:
        return SOURCE_QUALITY_WEIGHTS["unknown"]
    
    max_quality = 0.0
    for url in source_urls:
        url_lower = url.lower()
        if any(domain in url_lower for domain in [".ru", ".com", ".org"]) and "houzz" in url_lower:
            quality = SOURCE_QUALITY_WEIGHTS["reputable_aggregator"]
        elif "official" in url_lower or "studio" in url_lower:
            quality = SOURCE_QUALITY_WEIGHTS["official_site"]
        elif "portfolio" in url_lower or "case" in url_lower:
            quality = SOURCE_QUALITY_WEIGHTS["verified_portfolio"]
        elif "price" in url_lower or "rate" in url_lower:
            quality = SOURCE_QUALITY_WEIGHTS["rate_card"]
        else:
            quality = SOURCE_QUALITY_WEIGHTS["unknown"]
        
        max_quality = max(max_quality, quality)
    
    return max_quality


def compute_recency_factor(date_verified_str: Optional[str]) -> float:
    """Compute recency factor: max(0, 1 - days_since_verification / 180)."""
    if not date_verified_str:
        return 0.0
    
    try:
        # Remove quotes if present
        date_verified_str = date_verified_str.strip('"\'')
        d = date.fromisoformat(date_verified_str)
        days_since = (date.today() - d).days
        return max(0.0, 1.0 - days_since / 180.0)
    except (ValueError, TypeError):
        return 0.0


def compute_cross_validation(source_count: int) -> float:
    """Compute cross-validation score: min(1.0, source_count / 3) × 0.8."""
    if source_count <= 0:
        return 0.0
    return min(1.0, source_count / 3.0) * 0.8


def compute_data_completeness(frontmatter: Dict[str, str], required_fields: List[str]) -> float:
    """Compute data completeness: filled_required_fields / total_required_fields."""
    if not required_fields:
        return 0.0
    
    filled = sum(1 for field in required_fields if frontmatter.get(field))
    return filled / len(required_fields)


def parse_list_field(value: str) -> List[str]:
    """Parse a YAML list field from string."""
    if not value:
        return []
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        # Simple YAML array parsing
        inner = value[1:-1]
        if not inner.strip():
            return []
        return [item.strip().strip('"\'') for item in inner.split(",")]
    return [value]


def compute_confidence_score(frontmatter: Dict[str, str]) -> float:
    """Compute overall confidence score for a record."""
    required_fields = [
        "competitor", "domain", "service_type", "price_tier",
        "price_range_rub", "source_urls", "date_verified", "status"
    ]
    
    # Source quality (30%)
    source_urls_raw = frontmatter.get("source_urls", "")
    source_urls = parse_list_field(source_urls_raw)
    source_quality = classify_source_quality(source_urls)
    
    # Recency factor (25%)
    date_verified = frontmatter.get("date_verified")
    recency_factor = compute_recency_factor(date_verified)
    
    # Cross-validation (25%)
    source_count = len(source_urls)
    cross_validation = compute_cross_validation(source_count)
    
    # Data completeness (20%)
    data_completeness = compute_data_completeness(frontmatter, required_fields)
    
    # Final score
    score = (
        source_quality * 0.3 +
        recency_factor * 0.25 +
        cross_validation * 0.25 +
        data_completeness * 0.2
    )
    
    return round(score, 3)


def get_confidence_label(score: float) -> str:
    """Get human-readable label for confidence score."""
    if score >= 0.8:
        return "High"
    elif score >= 0.6:
        return "Medium"
    elif score >= 0.4:
        return "Low"
    else:
        return "Critical"


def main(update_frontmatter: bool = False) -> None:
    """Main function to compute confidence scores."""
    results = []
    
    # Process verified directory
    if not VERIFIED_DIR.exists():
        print(f"⚠️ Directory not found: {VERIFIED_DIR}")
        return
    
    for md_file in sorted(VERIFIED_DIR.glob("*.md")):
        if md_file.name.lower() == "readme.md":
            continue
        
        content = md_file.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)
        
        if not frontmatter:
            print(f"⚠️ No frontmatter: {md_file.relative_to(ROOT)}")
            continue
        
        score = compute_confidence_score(frontmatter)
        label = get_confidence_label(score)
        
        results.append({
            "file": md_file.name,
            "competitor": frontmatter.get("competitor", "UNKNOWN"),
            "score": score,
            "label": label
        })
        
        if update_frontmatter:
            # Update frontmatter with confidence_score
            new_fm_line = f"confidence_score: {score}"
            if "confidence_score:" not in content:
                # Insert before the closing ---
                end_idx = content.find("\n---\n", 4)
                if end_idx != -1:
                    new_content = content[:end_idx] + "\n" + new_fm_line + content[end_idx:]
                    md_file.write_text(new_content, encoding="utf-8")
                    print(f"✓ Updated {md_file.name}: confidence_score = {score}")
    
    # Print summary
    print("\n" + "="*60)
    print("CONFIDENCE SCORE SUMMARY")
    print("="*60)
    
    if not results:
        print("No records processed.")
        return
    
    high_count = sum(1 for r in results if r["label"] == "High")
    medium_count = sum(1 for r in results if r["label"] == "Medium")
    low_count = sum(1 for r in results if r["label"] == "Low")
    critical_count = sum(1 for r in results if r["label"] == "Critical")
    
    print(f"\nTotal records: {len(results)}")
    print(f"  High (≥0.8):     {high_count}")
    print(f"  Medium (0.6-0.8): {medium_count}")
    print(f"  Low (0.4-0.6):    {low_count}")
    print(f"  Critical (<0.4):  {critical_count}")
    
    print("\nDetailed results:")
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        print(f"  {r['score']:.3f} [{r['label']:8}] - {r['competitor']} ({r['file']})")


if __name__ == "__main__":
    import sys
    update_fm = "--update-frontmatter" in sys.argv
    main(update_fm)
