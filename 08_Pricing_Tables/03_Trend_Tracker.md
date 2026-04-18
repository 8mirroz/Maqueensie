---
doc_id: trend_tracker
doc_type: dataview_dashboard
status: active
date_added: 2026-04-17
date_verified: 2026-04-17
tags: [trends, tracker, dataview]
---

# Trend Tracker

Tracked vectors: emerging materials, layout innovations, smart-integration, bathroom ergonomics, commercial adaptations.

## Dynamic Trend Feed

```dataview
TABLE domain,
      competitor,
      service_type,
      tech_aesthetic_features,
      tags,
      date_verified,
      source_urls
FROM ""
WHERE (
  startswith(file.folder, "01_Architecture") OR
  startswith(file.folder, "02_Interior") OR
  startswith(file.folder, "03_Renovation") OR
  startswith(file.folder, "04_Decor") OR
  startswith(file.folder, "05_Furniture") OR
  startswith(file.folder, "06_RealEstate")
)
AND (
  contains(tags, "trend/materials") OR
  contains(tags, "trend/layout") OR
  contains(tags, "trend/smart") OR
  contains(tags, "trend/bathroom") OR
  contains(tags, "trend/commercial")
)
SORT date_verified DESC
```

## Fallback Manual Table

| Trend Theme | Domain | Competitor | Signal | Source | Date Verified |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
