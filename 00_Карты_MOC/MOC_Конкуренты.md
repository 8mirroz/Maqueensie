# Competitors MOC

```dataview
TABLE file.link AS Profile, domain, service_type, date_verified, status
FROM "07_Competitors" OR "03_Renovation"
WHERE type = "competitor_matrix" OR type = "competitor_profile"
SORT date_verified DESC
```
