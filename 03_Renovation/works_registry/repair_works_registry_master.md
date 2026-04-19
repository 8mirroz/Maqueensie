---
doc_id: repair_works_registry_master
doc_type: canonical_registry_table
system_role: source_of_truth_repair_normatives
version: 1.0.0
currency: RUB
geo_scope_default: [Moscow, Moscow_Oblast]
status: active
date_added: 2026-04-18
date_verified: 2026-04-18
tags: [renovation, registry, normatives, pricing, governance]
interfaces:
  reads_from: []
  exports_to:
    - "08_Pricing_Tables/04_Repair_Price_Matrix.md"
    - "03_Renovation/projects/"
dependencies:
  - "Obsidian Dataview plugin"
  - "Manual curation or scraper ingestion pipeline"
responsibilities:
  - "Store normalized unit prices for repair works"
  - "Define material consumption norms per work type"
  - "Provide traceability to source data (URLs, contracts)"
  - "Support tier mapping (Budget/Business/Premium)"
success_criteria:
  - "Every work item has unique work_id"
  - "Price ranges validated against min/max logic"
  - "Material norms present for >=80% of items"
  - "Source count >=2 for 'Verified' status"
governance:
  allowed_categories: [demolition, preparation, walls, floors, ceilings, electrical, plumbing, finishing, cleaning, packages, smart_home, supervision]
  allowed_units: [m2, m_pog, item, hour, kg, liter, zone, project, month, visit]
  allowed_statuses: [active, candidate, deprecated, archived]
  review_cycle_days: 30
  snapshot_path: "08_Pricing_Tables/snapshots/repair/"
---

# Repair Works Registry — Master Table

## System Purpose

Эталонный реестр работ и нормативов для ремонтно-строительных услуг.
Служит источником истины для:
- расчета смет проектов (`03_Renovation/projects/`)
- формирования матриц цен (`08_Pricing_Tables/04_Repair_Price_Matrix.md`)
- анализа себестоимости и маржинальности
- кросс-валидации с конкурентами

## Data Contract

### Required Columns

| Column | Type | Description | Validation |
|--------|------|-------------|------------|
| `work_id` | string | Уникальный идентификатор (RW-XXX-NNN) | Starts with `RW-` |
| `category` | enum | Категория работ | From allowed_categories |
| `work_name` | string | Наименование работы | Non-empty |
| `unit` | enum | Единица измерения | From allowed_units |
| `budget_min_rub` | number | Мин. цена Budget tier | >= 0, < business_min |
| `budget_max_rub` | number | Макс. цена Budget tier | >= budget_min |
| `business_min_rub` | number | Мин. цена Business tier | > budget_max |
| `business_max_rub` | number | Макс. цена Business tier | >= business_min |
| `premium_min_rub` | number | Мин. цена Premium tier | > business_max |
| `premium_max_rub` | number | Макс. цена Premium tier | >= premium_min |
| `material_norm` | string | Норма расхода материалов | Optional, recommended |
| `labor_hours` | number | Нормо-часы на единицу | >= 0 |
| `source_count` | number | Количество источников | >= 1 |
| `source_urls` | string | URL источников (;-separated) | Non-empty if source_count > 0 |
| `status` | enum | Статус записи | From allowed_statuses |
| `date_verified` | date | Дата последней проверки | YYYY-MM-DD |
| `notes` | string | Примечания | Optional |

### Tier Validation Rules

1. **Non-overlapping**: `budget_max < business_min <= business_max < premium_min <= premium_max`
2. **Positive ranges**: All min <= max within tier
3. **Status gate**: `status=active` только если `source_count >= 2`
4. **Unit consistency**: Цены соответствуют единице измерения (m2 vs item)

## Master Registry Table

| work_id | category | work_name | unit | budget_min_rub | budget_max_rub | business_min_rub | business_max_rub | premium_min_rub | premium_max_rub | material_norm | labor_hours | source_count | source_urls | status | date_verified | notes |
|---------|----------|-----------|------|----------------|----------------|------------------|------------------|-----------------|-----------------|---------------|-------------|--------------|-------------|--------|---------------|-------|
| RW-DEM-001 | demolition | Демонтаж перегородок (кирпич) | m2 | 350 | 550 | 551 | 850 | 851 | 1200 | - | 0.5 | 3 | https://remont-studio.ru/demontazh; https://stroyka-msk.ru/prices | active | 2026-04-17 | Включает вынос мусора в контейнер |
| RW-DEM-002 | demolition | Демонтаж стяжки до 5см | m2 | 250 | 400 | 401 | 650 | 651 | 950 | - | 0.4 | 2 | https://master-remont.ru/ceny; https://remont-studio.ru/demontazh | active | 2026-04-17 | Механизированный способ |
| RW-DEM-003 | demolition | Снятие обоев | m2 | 80 | 150 | 151 | 250 | 251 | 400 | - | 0.15 | 2 | https://stroyka-msk.ru/prices; https://fix-price-remont.ru | active | 2026-04-17 | Без обработки поверхности |
| RW-PREP-001 | preparation | Грунтовка стен | m2 | 60 | 100 | 101 | 180 | 181 | 300 | 0.2л/m2 | 0.1 | 3 | https://remont-studio.ru/grunt; https://master-remont.ru/ceny; https://stroyka-msk.ru/prices | active | 2026-04-17 | Глубокого проникновения |
| RW-PREP-002 | preparation | Штукатурка по маякам | m2 | 450 | 650 | 651 | 950 | 951 | 1400 | 25кг/10m2 | 0.8 | 4 | https://remont-studio.ru/shtukaturka; https://master-remont.ru/ceny; https://stroyka-msk.ru/prices; https://elite-otdelka.ru | active | 2026-04-17 | Гипсовая смесь, толщина до 20мм |
| RW-PREP-003 | preparation | Шпатлевка под обои (2 слоя) | m2 | 200 | 320 | 321 | 500 | 501 | 750 | 1.5кг/m2 | 0.4 | 3 | https://master-remont.ru/ceny; https://stroyka-msk.ru/prices; https://fix-price-remont.ru | active | 2026-04-17 | Финишная шпатлевка |
| RW-WALL-001 | walls | Кладка кирпича (перегородка) | m2 | 1200 | 1600 | 1601 | 2200 | 2201 | 3200 | 50шт/m2 | 1.2 | 3 | https://remont-studio.ru/kladka; https://master-remont.ru/ceny; https://stroyka-msk.ru/prices | active | 2026-04-17 | Полнотелый кирпич, армирование |
| RW-WALL-002 | walls | Возведение ГКЛ (1 слой) | m2 | 550 | 800 | 801 | 1200 | 1201 | 1700 | 2.1м2 ГКЛ/m2 | 0.6 | 3 | https://master-remont.ru/gkl; https://stroyka-msk.ru/prices; https://remont-studio.ru/kladka | active | 2026-04-17 | Каркас металлический, звукоизоляция |
| RW-FLOOR-001 | floors | Стяжка пола (до 5см) | m2 | 400 | 600 | 601 | 900 | 901 | 1300 | 25кг/10m2 | 0.5 | 4 | https://remont-studio.ru/styazhka; https://master-remont.ru/ceny; https://stroyka-msk.ru/prices; https://pol-master.ru | active | 2026-04-17 | Полусухая механизированная |
| RW-FLOOR-002 | floors | Укладка ламината | m2 | 250 | 400 | 401 | 650 | 651 | 950 | - | 0.3 | 3 | https://master-remont.ru/laminat; https://stroyka-msk.ru/prices; https://pol-master.ru | active | 2026-04-17 | С подложкой, без плинтуса |
| RW-FLOOR-003 | floors | Укладка плитки керамической | m2 | 800 | 1200 | 1201 | 1800 | 1801 | 2800 | 1.1м2 плитки/m2 | 0.9 | 4 | https://remont-studio.ru/plitka; https://master-remont.ru/ceny; https://stroyka-msk.ru/prices; https://elite-otdelka.ru | active | 2026-04-17 | Стандартная раскладка, затирка включена |
| RW-CEIL-001 | ceilings | Подвесной потолок ГКЛ | m2 | 600 | 900 | 901 | 1400 | 1401 | 2000 | 2.1м2 ГКЛ/m2 | 0.7 | 3 | https://master-remont.ru/potolki; https://stroyka-msk.ru/prices; https://remont-studio.ru/potolki | active | 2026-04-17 | Одноуровневый, каркас металлический |
| RW-CEIL-002 | ceilings | Натяжной потолок (ПВХ) | m2 | 350 | 550 | 551 | 850 | 851 | 1300 | - | 0.4 | 3 | https://potolok-msk.ru/ceny; https://master-remont.ru/potolki; https://stroyka-msk.ru/prices | active | 2026-04-17 | Матовый, стандартный монтаж |
| RW-ELEC-001 | electrical | Штробление стен (бетон) | m.пог | 250 | 400 | 401 | 650 | 651 | 950 | - | 0.3 | 2 | https://elektrik-moskva.ru/uslugi; https://remont-studio.ru/elektrika | active | 2026-04-17 | Алмазное штробление |
| RW-ELEC-002 | electrical | Прокладка кабеля | m.пог | 80 | 130 | 131 | 220 | 221 | 350 | - | 0.15 | 3 | https://elektrik-moskva.ru/uslugi; https://master-remont.ru/elektrika; https://stroyka-msk.ru/prices | active | 2026-04-17 | Кабель ВВГнг, гофра включена |
| RW-ELEC-003 | electrical | Установка розетки/выключателя | item | 250 | 400 | 401 | 650 | 651 | 950 | - | 0.2 | 3 | https://elektrik-moskva.ru/uslugi; https://master-remont.ru/elektrika; https://fix-price-remont.ru | active | 2026-04-17 | Внутренний монтаж, подрозетник включен |
| RW-PLUMB-001 | plumbing | Разводка труб водоснабжения | m.пог | 400 | 650 | 651 | 1000 | 1001 | 1500 | 1.2м трубы/m.пог | 0.5 | 3 | https://santehnik-profi.ru/ceny; https://remont-studio.ru/santehnika; https://stroyka-msk.ru/prices | active | 2026-04-17 | Полипропилен, сварка |
| RW-PLUMB-002 | plumbing | Установка сантехприборов | item | 800 | 1500 | 1501 | 2500 | 2501 | 4000 | - | 1.0 | 3 | https://santehnik-profi.ru/ceny; https://master-remont.ru/santehnika; https://santeh-moskva.ru | active | 2026-04-17 | Унитаз/раковина/смеситель |
| RW-FIN-001 | finishing | Поклейка обоев | m2 | 200 | 350 | 351 | 550 | 551 | 850 | 1.1 рулон/5m2 | 0.25 | 4 | https://remont-studio.ru/oboi; https://master-remont.ru/ceny; https://stroyka-msk.ru/prices; https://fix-price-remont.ru | active | 2026-04-17 | Виниловые/флизелиновые |
| RW-FIN-002 | finishing | Покраска стен (2 слоя) | m2 | 250 | 400 | 401 | 650 | 651 | 1000 | 0.3л/m2 | 0.35 | 3 | https://master-remont.ru/pokraska; https://stroyka-msk.ru/prices; https://elite-otdelka.ru | active | 2026-04-17 | Водоэмульсионная краска |
| RW-FIN-003 | finishing | Укладка плинтуса | m.пог | 100 | 180 | 181 | 300 | 301 | 500 | - | 0.15 | 2 | https://master-remont.ru/plintus; https://stroyka-msk.ru/prices | active | 2026-04-17 | Пластиковый, с кабель-каналом |
| RW-CLEAN-001 | cleaning | Клининг после ремонта | m2 | 80 | 130 | 131 | 220 | 221 | 350 | - | 0.2 | 2 | https://cleaning-msk.ru/remont; https://eco-clean.ru/ceny | active | 2026-04-17 | Влажная уборка, удаление пыли |
| RW-PKG-001 | packages | Пакет «Старт» (косметический) | m2 | 4500 | 5500 | 5501 | 7500 | 7501 | 9500 | Комплекс материалов | 10.0 | 3 | https://fix-price-remont.ru/packages; https://remont-studio.ru/kompleks; https://master-remont.ru/pakety | active | 2026-04-18 | Демонтаж, подготовка, обои, ламинат, базовая электрика |
| RW-PKG-002 | packages | Пакет «Оптима» (капитальный базовый) | m2 | 7500 | 9500 | 9501 | 13000 | 13001 | 16500 | Комплекс материалов | 18.0 | 3 | https://fix-price-remont.ru/packages; https://remont-studio.ru/kompleks; https://master-remont.ru/pakety | active | 2026-04-18 | Стяжка, плитка, сантехника, покраска, розетки |
| RW-PKG-003 | packages | Пакет «Комфорт» (капитальный расширенный) | m2 | 13000 | 16000 | 16001 | 20000 | 20001 | 26000 | Комплекс материалов премиум | 25.0 | 3 | https://fix-price-remont.ru/packages; https://remont-studio.ru/kompleks; https://elite-otdelka.ru/services | active | 2026-04-18 | Дизайнерские решения, сложные потолки, декор |
| RW-PKG-004 | packages | Пакет «Премиум» (дизайнерский) | m2 | 25000 | 35000 | 35001 | 50000 | 50001 | 80000+ | Материалы luxury сегмента | 40.0 | 2 | https://elite-otdelka.ru/services; https://remont-studio.ru/design | candidate | 2026-04-18 | Авторский надзор, умный дом, эксклюзивные материалы |
| RW-ELEC-005 | electrical | Сборка электрощита с автоматами | item | 4000 | 7000 | 7001 | 12000 | 12001 | 18000 | Щит + автоматы | 4.0 | 3 | https://elektrik-moskva.ru/shchity; https://remont-studio.ru/elektrika; https://master-remont.ru/elektro | active | 2026-04-18 | До 24 модулей, сборка по схеме |
| RW-ELEC-006 | electrical | Монтаж теплого пола (электрический) | m2 | 400 | 700 | 701 | 1100 | 1101 | 1700 | Кабель/маты, терморегулятор | 0.6 | 3 | https://elektrik-moskva.ru/teply-pol; https://remont-studio.ru/elektrika; https://pol-master.ru | active | 2026-04-18 | Укладка, подключение, тестирование |
| RW-ELEC-007 | electrical | Подключение бытовой техники | item | 300 | 600 | 601 | 1000 | 1001 | 1800 | - | 0.3 | 2 | https://master-remont.ru/bytovaya; https://remont-studio.ru/podklyuchenie | active | 2026-04-18 | Стиральная машина, посудомойка, духовка |
| RW-PLUMB-003 | plumbing | Монтаж водяного теплого пола | m2 | 800 | 1300 | 1301 | 2000 | 2001 | 3200 | Трубы, коллектор, изоляция | 1.2 | 3 | https://santehnik-profi.ru/teply-pol; https://remont-studio.ru/santehnika; https://pol-master.ru | active | 2026-04-18 | Раскладка, укладка, опрессовка |
| RW-PLUMB-004 | plumbing | Установка водонагревателя | item | 2500 | 4000 | 4001 | 6500 | 6501 | 10000 | Крепеж, подводка | 1.5 | 3 | https://santehnik-profi.ru/vodonagrevatel; https://remont-studio.ru/santehnika; https://master-remont.ru/santeh | active | 2026-04-18 | Накопительный/проточный, обвязка |
| RW-PLUMB-005 | plumbing | Монтаж систем фильтрации воды | item | 3000 | 5000 | 5001 | 8000 | 8001 | 13000 | Фильтры, картриджи | 2.0 | 2 | https://santehnik-profi.ru/filtraciya; https://remont-studio.ru/santehnika | active | 2026-04-18 | Магистральные фильтры, умягчители |
| RW-SMART-001 | smart_home | Установка умных розеток и выключателей | item | 800 | 1300 | 1301 | 2000 | 2001 | 3200 | Умные устройства | 0.3 | 2 | https://smart-home-msk.ru/ceny; https://elite-otdelka.ru/smart | candidate | 2026-04-18 | Настройка, интеграция в систему |
| RW-SMART-002 | smart_home | Монтаж датчиков (движение, протечка, свет) | item | 600 | 1000 | 1001 | 1600 | 1601 | 2600 | Датчики, крепление | 0.2 | 2 | https://smart-home-msk.ru/ceny; https://elektrik-moskva.ru/smart | candidate | 2026-04-18 | Установка, калибровка, тестирование |
| RW-SMART-003 | smart_home | Настройка умного освещения | зона | 2000 | 3500 | 3501 | 5500 | 5501 | 9000 | Контроллеры, ленты | 1.0 | 2 | https://smart-home-msk.ru/light; https://elite-otdelka.ru/smart | candidate | 2026-04-18 | Сценарии, расписание, голосовое управление |
| RW-FIN-004 | finishing | Венецианская штукатурка | m2 | 1200 | 1800 | 1801 | 2800 | 2801 | 4500 | Штукатурка, воск, инструменты | 1.5 | 3 | https://elite-otdelka.ru/decor; https://master-remont.ru/venecianka; https://decor-studio.ru | candidate | 2026-04-18 | Многослойное нанесение, полировка |
| RW-FIN-005 | finishing | Нанесение фактурной краски | m2 | 600 | 950 | 951 | 1500 | 1501 | 2400 | Краска, валики, штампы | 0.8 | 2 | https://master-remont.ru/faktura; https://elite-otdelka.ru/decor | candidate | 2026-04-18 | Создание текстуры, защитное покрытие |
| RW-FIN-006 | finishing | Монтаж декоративного камня | m2 | 1500 | 2300 | 2301 | 3500 | 3501 | 5500 | Камень, клей, затирка | 1.2 | 2 | https://stone-master.ru/montazh; https://elite-otdelka.ru/decor | candidate | 2026-04-18 | Раскрой, укладка, герметизация |
| RW-SUPER-001 | supervision | Разовый выезд технического инженера | выезд | 3000 | 5000 | 5001 | 8000 | 8001 | 12000 | - | 2.0 | 3 | https://engineer-nadzor.ru/ceny; https://elite-otdelka.ru/nadzor; https://remont-expert.ru | candidate | 2026-04-18 | Проверка качества, дефектовка, отчет |
| RW-SUPER-002 | supervision | Сопровождение проекта (месяц) | месяц | 25000 | 40000 | 40001 | 65000 | 65001 | 100000 | - | 20.0 | 2 | https://engineer-nadzor.ru/ceny; https://elite-otdelka.ru/nadzor | candidate | 2026-04-18 | Еженедельные проверки, приемка этапов |
| RW-SUPER-003 | supervision | Полный цикл технического надзора | проект | 80000 | 150000 | 150001 | 250000 | 250001 | 400000 | - | 60.0 | 2 | https://engineer-nadzor.ru/full; https://elite-otdelka.ru/nadzor | candidate | 2026-04-18 | От старта до сдачи, все этапы |

## Validation Diagnostics

```dataviewjs
const SOURCE_PATH = "03_Renovation/works_registry/repair_works_registry_master.md";
const ALLOWED_CATEGORIES = new Set(["demolition", "preparation", "walls", "floors", "ceilings", "electrical", "plumbing", "finishing", "cleaning", "packages", "smart_home", "supervision"]);
const ALLOWED_UNITS = new Set(["m2", "m_pog", "item", "hour", "kg", "liter", "zone", "project", "month", "visit"]);
const ALLOWED_STATUSES = new Set(["active", "candidate", "deprecated", "archived"]);

function sanitizeNumber(value) {
  if (value === null || value === undefined) return NaN;
  const cleaned = String(value).replace(/\u00A0/g, " ").replace(/\s+/g, "").replace(/,/g, ".").replace(/[^\d.\-]/g, "");
  return cleaned ? Number(cleaned) : NaN;
}

function parseRow(line) {
  return line.split("|").slice(1, -1).map(v => v.trim());
}

function isSeparatorRow(cells) {
  return cells.every(c => /^:?-{3,}:?$/.test(c.replace(/\s+/g, "")));
}

let raw;
try {
  raw = await dv.io.load(SOURCE_PATH);
} catch (e) {
  dv.header(3, "Registry Validation Error");
  dv.paragraph(`Cannot load source: ${SOURCE_PATH}`);
  dv.paragraph(String(e));
  return;
}

if (!raw || !raw.trim()) {
  dv.header(3, "Registry Validation Error");
  dv.paragraph("Source file is empty.");
  return;
}

const tableLines = raw.split("\n").map(l => l.trim()).filter(l => l.startsWith("|"));
if (tableLines.length < 3) {
  dv.header(3, "Registry Validation Error");
  dv.paragraph("No valid markdown table found.");
  return;
}

const headers = parseRow(tableLines[0]);
const headerSet = new Set(headers);
const requiredCols = ["work_id", "category", "work_name", "unit", "budget_min_rub", "budget_max_rub", "business_min_rub", "business_max_rub", "premium_min_rub", "premium_max_rub", "source_count", "status"];
const missingCols = requiredCols.filter(c => !headerSet.has(c));

if (missingCols.length) {
  dv.header(3, "Schema Error");
  dv.paragraph(`Missing required columns: ${missingCols.join(", ")}`);
  return;
}

const issues = [];
const stats = { total: 0, active: 0, candidate: 0, invalid_tier: 0, invalid_enum: 0, low_sources: 0 };

for (const line of tableLines.slice(1)) {
  const cells = parseRow(line);
  if (!cells.length || isSeparatorRow(cells)) continue;
  
  const row = Object.fromEntries(headers.map((h, i) => [h, cells[i] ?? ""]));
  stats.total++;
  
  if (!row.work_id || !row.work_id.startsWith("RW-")) {
    issues.push(`[${row.work_id || "UNKNOWN"}] Invalid work_id format (must start with RW-)`);
    continue;
  }
  
  if (!ALLOWED_CATEGORIES.has(row.category)) {
    issues.push(`[${row.work_id}] Invalid category: "${row.category}"`);
    stats.invalid_enum++;
  }
  
  if (!ALLOWED_UNITS.has(row.unit)) {
    issues.push(`[${row.work_id}] Invalid unit: "${row.unit}"`);
    stats.invalid_enum++;
  }
  
  if (!ALLOWED_STATUSES.has(row.status)) {
    issues.push(`[${row.work_id}] Invalid status: "${row.status}"`);
    stats.invalid_enum++;
  }
  
  const bmin = sanitizeNumber(row.budget_min_rub);
  const bmax = sanitizeNumber(row.budget_max_rub);
  const busmin = sanitizeNumber(row.business_min_rub);
  const busmax = sanitizeNumber(row.business_max_rub);
  const pmin = sanitizeNumber(row.premium_min_rub);
  const pmax = sanitizeNumber(row.premium_max_rub);
  
  const tierValid = Number.isFinite(bmin) && Number.isFinite(bmax) && Number.isFinite(busmin) && 
                    Number.isFinite(busmax) && Number.isFinite(pmin) && Number.isFinite(pmax);
  
  if (!tierValid) {
    issues.push(`[${row.work_id}] Invalid numeric values in tier ranges`);
    stats.invalid_tier++;
    continue;
  }
  
  if (!(bmax < busmin && busmax < pmin && pmin <= pmax && bmin <= bmax && busmin <= busmax)) {
    issues.push(`[${row.work_id}] Tier overlap detected: Budget[${bmin}-${bmax}] Business[${busmin}-${busmax}] Premium[${pmin}-${pmax}]`);
    stats.invalid_tier++;
  }
  
  if (row.status === "active") {
    stats.active++;
    const srcCount = sanitizeNumber(row.source_count);
    if (!Number.isFinite(srcCount) || srcCount < 2) {
      issues.push(`[${row.work_id}] Active status requires source_count >= 2 (got ${srcCount})`);
      stats.low_sources++;
    }
  } else if (row.status === "candidate") {
    stats.candidate++;
  }
}

dv.header(3, "Registry Diagnostics");
dv.paragraph(`Total records: ${stats.total} | Active: ${stats.active} | Candidate: ${stats.candidate}`);
dv.paragraph(`Validation errors: Tier overlap=${stats.invalid_tier} | Invalid enums=${stats.invalid_enum} | Low sources=${stats.low_sources}`);

if (issues.length > 0) {
  dv.header(4, "Validation Issues");
  dv.list(issues.slice(0, 20));
  if (issues.length > 20) {
    dv.paragraph(`... and ${issues.length - 20} more issues`);
  }
} else {
  dv.paragraph("**✓ All validation checks passed**");
}
```

## Governance & Update Protocol

### Обновление реестра

1. **Добавление новой работы**:
   - Присвоить уникальный `work_id` по шаблону `RW-{CATEGORY}-{NNN}`
   - Заполнить все обязательные поля
   - Указать минимум 2 источника для статуса `active`
   - Проверить непересекаемость тир-диапазонов

2. **Изменение цен**:
   - При изменении любого порога >10% — перепроверить источники
   - Если `date_verified` > 30 дней — перевести в `candidate` до ревизии
   - Логировать изменения в `tier_rules_changelog.md`

3. **Архивация**:
   - При устаревании технологии — статус `deprecated`
   - Перенос в архив через 180 дней после `deprecated`

### Snapshot Rules

- Перед массовым обновлением создавать снапшот: `08_Pricing_Tables/snapshots/repair/registry_snapshot_YYYY-MM-DD.md`
- Снапшот содержит полную копию таблицы + хеш-сумму
- Хранить минимум 4 последних снапшота (квартальная история)

## Evolution Path

### v1.1 (Planned)
- Добавить колонку `complexity_factor` для учета сложности объектов
- Внедрить `region_coefficient` для масштабирования на другие регионы
- Связь с проектами через `project_id` в заметках проектов

### v1.2 (Planned)
- Интеграция со скраперами для авто-обновления цен
- Расчет confidence score на основе recency + source quality
- Детекция аномалий цен (IQR метод)

### v2.0 (Target)
- Переход на JSON/JSONL формат для версионирования
- REST API для внешнего доступа
- Исторические тренды цен по категориям

## Manual Fallback

Если Dataview не работает, использовать статичную таблицу выше.
Актуальность данных проверять по `date_verified`.
