---
doc_id: competitor_comparison_dashboard
doc_type: dataview_dashboard
status: active
date_added: 2026-04-17
date_verified: 2026-04-17
tags: [competitors, dashboard, dataview]
---

# Competitor Comparison Dashboard

## Dynamic Comparison (from `07_Competitors`)

```dataview
TABLE competitor AS Competitor,
      domain AS Domain,
      service_type AS Service,
      hook AS Hook,
      tech_aesthetic_features AS Tech_Aesthetic,
      price_tier AS Tier,
      price_range_rub AS Price_Range,
      source_urls AS Sources,
      date_verified AS Verified
FROM "07_Competitors"
WHERE status = "Verified" OR status = "Pending"
SORT domain ASC, competitor ASC
```

## Pricing Overlap View

```dataview
TABLE competitor,
      service_type,
      price_tier,
      price_range_rub,
      choice(price_range_rub[0] <= 0 OR price_range_rub[1] <= 0, "check", "ok") AS range_quality
FROM "07_Competitors"
WHERE contains(tags, "pricing") OR contains(tags, "competitor")
SORT competitor ASC
```

## Fallback Manual Table

| Competitor | Domain | Hook | Tech/Aesthetic Features | Tier | Price Range (RUB) | Sources |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
