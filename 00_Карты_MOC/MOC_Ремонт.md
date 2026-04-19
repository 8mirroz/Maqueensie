# Renovation MOC (Global Index)

> См. детализированный дашборд: [[Renovation_MOC|MOC — Ремонт и Отделка (2026)]]

## 🏗 Market Intelligence
```dataview
TABLE type as Type, region as Region, tags as Tags
FROM "03_Renovation"
WHERE type = "market_map" OR type = "demand_map"
SORT updated DESC
```

## 💰 Pricing & Competitors
```dataview
TABLE type as Type, region as Region
FROM "03_Renovation"
WHERE type = "pricing_table" OR type = "competitor_matrix" OR type = "offers_library"
SORT type ASC
```
