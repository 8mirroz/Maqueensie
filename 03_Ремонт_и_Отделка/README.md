# Renovation Domain — System Overview

## Purpose

Подсистема управления ремонтно-строительными проектами в рамках Pricing Intelligence OS.
Обеспечивает полный цикл от нормативов цен до смет проектов и аналитики.

## Structure

```
03_Renovation/
├── README.md                          # Этот файл
├── ARCHITECTURE.md                    # Системная архитектура
├── works_registry/
│   └── repair_works_registry_master.md  # Эталонный реестр работ (Source of Truth)
├── projects/
│   ├── project_template.md            # Шаблон сметы проекта
│   └── PROJ-YYYY-NNN_*.md             # Актуальные проекты
└── costs/                             # Анализ себестоимости (future)
```

## Key Artifacts

| Artifact | Role | Location |
|----------|------|----------|
| **Repair Works Registry** | Source of Truth для всех цен на работы | `works_registry/repair_works_registry_master.md` |
| **Price Matrix Dashboard** | Operational view с валидацией | `08_Pricing_Tables/04_Repair_Price_Matrix.md` |
| **Project Template** | Шаблон для создания смет | `projects/project_template.md` |
| **Snapshots** | Исторические версии данных | `08_Pricing_Tables/snapshots/repair/` |

## Data Flow

1. **Input:** Внешние источники (сайты, договоры, прайсы) → ручная курация или скраперы
2. **Storage:** Repair Works Registry (эталонные данные с валидацией)
3. **Processing:** Price Matrix Dashboard (агрегация, группировка, диагностика)
4. **Output:** Проектные сметы, экспорт в snapshots, аналитика

## Governance

### Controlled Vocabularies

- **Categories:** demolition, preparation, walls, floors, ceilings, electrical, plumbing, finishing, cleaning
- **Units:** m2, m_pog, item, hour, kg, liter
- **Statuses:** active, candidate, deprecated, archived
- **Tiers:** Budget_Ready, Business, Premium_Ultra

### Quality Gates

- ✅ Все active записи имеют `source_count >= 2`
- ✅ Нет пересечений тир-диапазонов
- ✅ Все категории/единицы из allowed list
- ✅ `date_verified` актуальна (<30 дней)

### Update Protocol

1. Добавление работы → уникальный work_id, >=2 источников
2. Изменение цен >10% → перепроверка, снапшот, changelog
3. Ревизия каждые 30 дней → иначе статус candidate

## Usage

### For Analysts

1. Открыть [[PRC_Матрица_цен_ремонт]] в Reading view
2. Проверить диагностику валидации
3. Экспортировать данные для сметы
4. Использовать [[project_template]] для расчета

### For Project Managers

1. Создать копию `project_template.md` с именем `PROJ-YYYY-NNN_ClientName.md`
2. Заполнить объемы работ по обмерам
3. Цены взять из Price Matrix по выбранному тиру
4. Сохранить итоговую смету в `projects/`

### For Data Stewards

1. Мониторить `date_verified` в реестре
2. При устаревании >30 дней — инициировать ревизию
3. Перед массовыми изменениями — создать снапшот
4. Логировать изменения в `tier_rules_changelog.md`

## Integration Points

| System | Direction | Purpose |
|--------|-----------|---------|
| [[tier_rules]] | ← reads | Общие правила тиров для всех доменов |
| [[GID_Правила_валидации]] | ← reads | Политики валидации данных |
| [[PRC_Матрица_цен_ремонт]] | → exports | Визуализация и экспорт данных |
| `08_Pricing_Tables/snapshots/repair/` | → exports | Архив исторических версий |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2026-04-18 | Initial release: registry (25 items), dashboard, template, architecture |

## References

- [[GID_Архитектура_ремонта]] — детальная системная архитектура
- [[DEV_План_развития_репозитория]] — стратегия развития
- [[PRC_Дашборд_сравнения_конкурентов]] — аналогичная система для конкурентов
