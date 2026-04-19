---
doc_id: renovation_system_architecture
doc_type: architecture_doc
system_role: system_design_repair_domain
version: 1.0.0
date_added: 2026-04-18
date_verified: 2026-04-18
tags: [renovation, architecture, system_design, documentation]

title: "Архитектура ремонта"---

# Renovation System Architecture

## Overview

Подсистема управления ремонтно-строительными проектами в рамках Pricing Intelligence OS.
Обеспечивает полный цикл: от нормативов цен → смета проекта → контроль исполнения → аналитика.

## System Context

```
┌─────────────────────────────────────────────────────────────────┐
│                    Pricing Intelligence OS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐     ┌──────────────────┐                 │
│  │  Tier Rules      │────▶│  Price Matrix    │                 │
│  │  (Architecture)  │     │  Dashboard       │                 │
│  └──────────────────┘     └──────────────────┘                 │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────┐                  │
│  │        REPAIR WORKS REGISTRY             │                  │
│  │  (Source of Truth for Renovation Domain) │                  │
│  │                                          │                  │
│  │  - 25+ work types                        │                  │
│  │  - 3-tier pricing (Budget/Business/Prem) │                  │
│  │  - Material norms                        │                  │
│  │  - Labor hours                           │                  │
│  │  - Source traceability                   │                  │
│  └──────────────────────────────────────────┘                  │
│           │                      │                             │
│           ▼                      ▼                             │
│  ┌──────────────────┐   ┌──────────────────┐                  │
│  │  Price Matrix    │   │  Project         │                  │
│  │  Dashboard       │   │  Templates       │                  │
│  │  (Visualization) │   │  (Estimation)    │                  │
│  └──────────────────┘   └──────────────────┘                  │
│                                │                               │
│                                ▼                               │
│                       ┌──────────────────┐                    │
│                       │  Actual Projects │                    │
│                       │  (03_Renovation/ │                    │
│                       │   projects/)     │                    │
│                       └──────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Repair Works Registry (`works_registry/repair_works_registry_master.md`)

**Role:** Source of Truth для всех данных по ремонтным работам

**Responsibilities:**
- Хранение эталонных цен по 3 тирам
- Нормативы расхода материалов
- Нормо-часы на единицу работы
- Трассируемость к источникам (URLs)
- Валидация непересекаемости тир-диапазонов

**Data Model:**
```yaml
work_id: RW-{CATEGORY}-{NNN}  # уникальный ID
category: enum                # категория работы
work_name: string             # наименование
unit: enum                    # ед. измерения
budget_min_rub: number        # диапазон Budget
budget_max_rub: number
business_min_rub: number      # диапазон Business
business_max_rub: number
premium_min_rub: number       # диапазон Premium
premium_max_rub: number
material_norm: string         # норма расхода материалов
labor_hours: number           # трудозатраты
source_count: number          # кол-во источников
source_urls: string[]         # URL источников
status: enum                  # active/candidate/deprecated
date_verified: date           # дата проверки
```

**Validation Rules:**
- `budget_max < business_min <= business_max < premium_min <= premium_max`
- `status=active` только при `source_count >= 2`
- Все числовые поля должны быть валидными
- Категория и единицы из контролируемого словаря

### 2. Price Matrix Dashboard (`08_Pricing_Tables/04_Repair_Price_Matrix.md`)

**Role:** Operational View для аналитики и экспорта

**Responsibilities:**
- Чтение данных из реестра
- Валидация и фильтрация записей
- Группировка по категориям
- Агрегация средних цен
- Диагностика ошибок
- Экспорт в snapshots

**Algorithm:**
```
1. Load source markdown table
2. Parse headers and rows
3. Validate schema (required columns)
4. For each row:
   - Check work_id format
   - Validate enum fields (category, unit, status)
   - Sanitize numeric values
   - Check tier non-overlap
   - Filter by status=active
5. Group by category
6. Calculate averages per tier
7. Render tables with diagnostics
8. Export issues list if any
```

**Fail-Safe Behavior:**
- При отсутствии файла — явная ошибка
- При пустом файле — явная ошибка
- При missing columns — список отсутствующих
- При invalid data — skip с логированием причины
- Никогда не падать silently

### 3. Project Templates (`projects/project_template.md`)

**Role:** Шаблон для создания смет проектов

**Responsibilities:**
- Структура WBS (Work Breakdown Structure)
- Формула расчета стоимости
- Привязка к реестру цен
- Timeline планирование
- Change log версионирование

**Integration Points:**
- Читает цены из Price Matrix
- Использует work_id из Registry
- Экспортирует итоговые сметы в `projects/`

### 4. Snapshots (`08_Pricing_Tables/snapshots/repair/`)

**Role:** Историческая версия данных

**Responsibilities:**
- Сохранение состояния реестра на дату
- Контрольные точки перед изменениями
- Основа для тренд-анализа

**Retention Policy:**
- Минимум 4 последних снапшота (квартал)
- Снапшот при каждом изменении tier-правил
- Хеш-сумма для верификации целостности

## Data Flow

```
┌─────────────────┐
│ External Sources│ (websites, contracts, rate cards)
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│ Manual Curation │────▶│  Repair Works    │
│ OR Scraper API  │     │  Registry        │
└─────────────────┘     └─────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
           ┌────────────┐ ┌────────────┐ ┌────────────┐
           │   Price    │ │  Project   │ │  Snapshot  │
           │   Matrix   │ │  Template  │ │  Archive   │
           └────────────┘ └────────────┘ └────────────┘
```

## Governance Model

### Controlled Vocabularies

**Categories:**
- `demolition`, `preparation`, `walls`, `floors`, `ceilings`
- `electrical`, `plumbing`, `finishing`, `cleaning`

**Units:**
- `m2`, `m_pog`, `item`, `hour`, `kg`, `liter`

**Statuses:**
- `active`, `candidate`, `deprecated`, `archived`

**Tiers:**
- `Budget_Ready`, `Business`, `Premium_Ultra`

### Update Protocol

1. **Добавление работы:**
   - Создать запись с уникальным `work_id`
   - Заполнить все required fields
   - Указать >=2 источников для `active`
   - Проверить непересекаемость тиров

2. **Изменение цен:**
   - При изменении >10% — перепроверить источники
   - Обновить `date_verified`
   - Создать снапшот до массовых изменений
   - Логировать в changelog

3. **Ревизия:**
   - Каждые 30 дней для `active` записей
   - Если >30 дней без проверки — статус `candidate`
   - Если >180 дней — статус `deprecated`

### Quality Gates

- [ ] Все active записи имеют `source_count >= 2`
- [ ] Нет пересечений тир-диапазонов
- [ ] Все категории из allowed list
- [ ] Все единицы из allowed list
- [ ] `date_verified` актуальна (<30 дней)
- [ ] Снапшот создан перед изменениями

## Evolution Roadmap

### v1.0 (Current) ✅
- Базовый реестр с 25 позициями
- Dataview дашборд с валидацией
- Проектный шаблон
- Snapshot структура

### v1.1 (Next)
- [ ] Добавить `complexity_factor` для сложных объектов
- [ ] Внедрить `region_coefficient` для других регионов
- [ ] Связь с конкретными проектами через `project_id`
- [ ] Расчет полной себестоимости (materials + labor)

### v1.2 (Planned)
- [ ] Интеграция со скраперами для авто-обновления
- [ ] Confidence scoring на основе recency + source quality
- [ ] Детекция аномалий цен (IQR метод)
- [ ] Автоматические алерты при отклонениях >20%

### v2.0 (Target)
- [ ] Переход на JSON/JSONL для версионирования
- [ ] REST API для внешнего доступа
- [ ] Исторические тренды цен по категориям
- [ ] Визуализация графиков (Chart.js integration)
- [ ] Экспорт в Excel/CSV для клиентов

## Risk Management

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Устаревание цен | High | Medium | 30-day review cycle, auto-alerts |
| Недостаточно источников | Medium | Low | Gate: min 2 sources for active |
| Ошибки ввода данных | Medium | Medium | Validation script, CI/CD checks |
| Потеря исторических данных | High | Low | Quarterly snapshots, hash verification |
| Некорректные сметы | High | Low | Template validation, cross-check with matrix |

## Success Metrics

- **Coverage:** >=90% типовых работ покрыто реестром
- **Freshness:** >=95% active записей проверены за последние 30 дней
- **Traceability:** 100% active записей имеют >=2 источника
- **Accuracy:** <5% расхождений между сметой и фактом
- **Adoption:** >=10 проектов используют систему

## References

- [[GID_Правила_валидации]] — общие правила валидации
- [[tier_rules]] — мастер-правила тиров
- [[PRC_Дашборд_сравнения_конкурентов]] — аналогичная система для конкурентов
- [[DEV_План_развития_репозитория]] — стратегия развития репозитория
