# Furniture MOC

```dataview
TABLE file.link AS Note, competitor, service_type, price_tier, date_verified, status
FROM "05_Furniture"
WHERE contains(tags, "service") OR contains(tags, "competitor")
SORT date_verified DESC
```
