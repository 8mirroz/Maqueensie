---
doc_id: renovation_project_template
doc_type: project_template
system_role: project_estimation_template
status: active
version: 1.0.0
date_added: 2026-04-18
tags: [renovation, project, template, estimate]
interfaces:
  reads_from:
    - "03_Renovation/works_registry/repair_works_registry_master.md"
    - "08_Pricing_Tables/04_Repair_Price_Matrix.md"
  exports_to:
    - "03_Renovation/projects/"
dependencies:
  - "Repair Works Registry"
  - "Price Matrix Dashboard"

title: "project template"---

# Project Template — Renovation Estimate

## Project Metadata

| Field | Value |
|-------|-------|
| **Project ID** | `PROJ-YYYY-NNN` |
| **Object Type** | apartment / house / commercial |
| **Area (m²)** |  |
| **Location** | Moscow / Moscow Oblast / Other |
| **Tier** | Budget_Ready / Business / Premium_Ultra |
| **Status** | planning / estimate / in_progress / completed |
| **Date Created** | YYYY-MM-DD |
| **Date Verified** | YYYY-MM-DD |

## Client Requirements

- [ ] Демонтаж старых покрытий
- [ ] Подготовка поверхностей
- [ ] Возведение перегородок
- [ ] Стяжка пола
- [ ] Электромонтажные работы
- [ ] Сантехнические работы
- [ ] Отделочные работы
- [ ] Клининг

## Estimate Calculation

### Formula

Для каждой категории работ:
```
Total = Σ (Quantity × Unit_Price_by_Tier) + Materials + Labor
```

Где:
- `Quantity` — объем работ из обмеров объекта
- `Unit_Price_by_Tier` — цена из реестра по выбранному тиру
- `Materials` — расход материалов по нормативам
- `Labor` — трудозатраты × ставку мастера

### Work Breakdown Structure

| Category | Work ID | Work Name | Unit | Quantity | Unit Price (₽) | Total (₽) | Material Norm | Material Cost (₽) | Labor Hours |
|----------|---------|-----------|------|----------|---------------:|----------:|---------------|------------------:|------------:|
| demolition | RW-DEM-001 | Демонтаж перегородок | m2 |  |  |  | - |  | 0.5 |
| demolition | RW-DEM-002 | Демонтаж стяжки | m2 |  |  |  | - |  | 0.4 |
| preparation | RW-PREP-001 | Грунтовка стен | m2 |  |  |  | 0.2л/m2 |  | 0.1 |
| preparation | RW-PREP-002 | Штукатурка по маякам | m2 |  |  |  | 25кг/10m2 |  | 0.8 |
| walls | RW-WALL-001 | Кладка кирпича | m2 |  |  |  | 50шт/m2 |  | 1.2 |
| floors | RW-FLOOR-001 | Стяжка пола | m2 |  |  |  | 25кг/10m2 |  | 0.5 |
| electrical | RW-ELEC-001 | Штробление стен | m.пог |  |  |  | - |  | 0.3 |
| electrical | RW-ELEC-002 | Прокладка кабеля | m.пог |  |  |  | - |  | 0.15 |
| plumbing | RW-PLUMB-001 | Разводка труб | m.пог |  |  |  | 1.2м трубы |  | 0.5 |
| finishing | RW-FIN-001 | Поклейка обоев | m2 |  |  |  | 1.1 рулон/5m2 |  | 0.25 |

*Цены брать из [[PRC_Матрица_цен_ремонт]] по выбранному тиру*

## Summary

| Component | Amount (₽) |
|-----------|-----------:|
| **Labor Total** |  |
| **Materials Total** |  |
| **Subtotal** |  |
| **Contingency (10%)** |  |
| **Grand Total** |  |

## Timeline

| Phase | Duration (days) | Start Date | End Date |
|-------|----------------:|------------|----------|
| Demolition |  |  |  |
| Preparation |  |  |  |
| Walls & Floors |  |  |  |
| Electrical & Plumbing |  |  |  |
| Finishing |  |  |  |
| Cleaning |  |  |  |

## Source Traceability

Все цены верифицированы по источникам:
- [[PRC_Мастер_реестр_ремонтных_работ]] — эталонный реестр
- Минимум 2 источника на каждую позицию (см. `source_urls` в реестре)
- Дата последней проверки: `date_verified`

## Change Log

| Date | Change | Author | Reason |
|------|--------|--------|--------|
|  | Initial estimate |  |  |

## Governance Notes

- Пересчитывать смету при изменении цен в реестре >10%
- Актуализировать `date_verified` каждые 30 дней
- Логировать все изменения в Change Log
- Финальная смета требует подтверждения клиентом
