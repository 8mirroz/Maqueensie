---
doc_id: repair_price_matrix
doc_type: dataview_dashboard
system_role: pricing_dashboard_repair
status: active
version: 1.0.0
date_added: 2026-04-18
date_verified: 2026-04-18
tags: [renovation, pricing, matrix, dataview, dashboard]
interfaces:
  reads_from:
    - "03_Renovation/works_registry/repair_works_registry_master.md"
  exports_to:
    - "08_Pricing_Tables/snapshots/repair/"
    - "03_Renovation/projects/"
dependencies:
  - "Obsidian Dataview plugin"
  - "Dataview JavaScript Queries enabled"
  - "repair_works_registry_master.md"
responsibilities:
  - "Render active repair works by category × tier"
  - "Aggregate price ranges from registry"
  - "Expose material norms and labor hours"
  - "Fail safely on missing or malformed input"
success_criteria:
  - "Dashboard renders without runtime crash"
  - "Only active valid records are included"
  - "Numeric fields sanitized before aggregation"
  - "Each row preserves work_id traceability"
governance:
  allowed_categories: [demolition, preparation, walls, floors, ceilings, electrical, plumbing, finishing, cleaning]
  allowed_statuses: [active, candidate, deprecated, archived]
  export_snapshot_path: "08_Pricing_Tables/snapshots/repair/"
  source_of_truth: "03_Renovation/works_registry/repair_works_registry_master.md"

title: "Матрица цен ремонт"---

# Repair Price Matrix — Category × Tier

## Purpose

Операционный дашборд для просмотра нормативов цен на ремонтно-строительные работы.
Агрегирует данные из эталонного реестра, группирует по категориям и тирам,
предоставляет диагностику валидации и экспорт для смет проектов.

## Dataview Plugin Setup

1. Obsidian Settings -> Community plugins -> install `Dataview`
2. Enable `JavaScript Queries` in Dataview settings
3. Open this note in Reading view

## Data Contract

Expected source file: `03_Renovation/works_registry/repair_works_registry_master.md`

Required table columns:
- `work_id`
- `category`
- `work_name`
- `unit`
- `budget_min_rub`, `budget_max_rub`
- `business_min_rub`, `business_max_rub`
- `premium_min_rub`, `premium_max_rub`
- `material_norm`
- `labor_hours`
- `source_count`
- `source_urls`
- `status`
- `date_verified`

Allowed `category` values:
- `demolition`, `preparation`, `walls`, `floors`, `ceilings`, `electrical`, `plumbing`, `finishing`, `cleaning`

## Dynamic Matrix

```dataviewjs
const SOURCE_PATH = "03_Renovation/works_registry/repair_works_registry_master.md";
const REQUIRED_COLUMNS = [
  "work_id", "category", "work_name", "unit",
  "budget_min_rub", "budget_max_rub",
  "business_min_rub", "business_max_rub",
  "premium_min_rub", "premium_max_rub",
  "material_norm", "labor_hours", "source_count", "source_urls", "status", "date_verified"
];
const ALLOWED_CATEGORIES = new Set(["demolition", "preparation", "walls", "floors", "ceilings", "electrical", "plumbing", "finishing", "cleaning"]);
const ACTIVE_STATUS = "active";

function sanitizeNumber(value) {
  if (value === null || value === undefined) return NaN;
  const cleaned = String(value)
    .replace(/\u00A0/g, " ")
    .replace(/\s+/g, "")
    .replace(/,/g, ".")
    .replace(/[^\d.\-]/g, "");
  return cleaned ? Number(cleaned) : NaN;
}

function parseRow(line) {
  return line.split("|").slice(1, -1).map(v => v.trim());
}

function isSeparatorRow(cells) {
  return cells.every(c => /^:?-{3,}:?$/.test(c.replace(/\s+/g, "")));
}

function normalizeSources(raw) {
  return String(raw || "")
    .split(";")
    .map(s => s.trim())
    .filter(Boolean);
}

let raw;
try {
  raw = await dv.io.load(SOURCE_PATH);
} catch (e) {
  dv.header(3, "Repair Price Matrix Error");
  dv.paragraph(`Source file could not be loaded: ${SOURCE_PATH}`);
  dv.paragraph(String(e));
  return;
}

if (!raw || !raw.trim()) {
  dv.header(3, "Repair Price Matrix Error");
  dv.paragraph(`Source file is empty: ${SOURCE_PATH}`);
  return;
}

const tableLines = raw
  .split("\n")
  .map(l => l.trim())
  .filter(l => l.startsWith("|"));

if (tableLines.length < 2) {
  dv.header(3, "Repair Price Matrix Error");
  dv.paragraph("No markdown table found in source file.");
  return;
}

const headers = parseRow(tableLines[0]);
const headerSet = new Set(headers);
const missingColumns = REQUIRED_COLUMNS.filter(c => !headerSet.has(c));

if (missingColumns.length) {
  dv.header(3, "Repair Price Matrix Error");
  dv.paragraph(`Missing required columns: ${missingColumns.join(", ")}`);
  return;
}

const records = [];
const issues = [];
let processedRows = 0;
let activeRows = 0;

for (const line of tableLines.slice(1)) {
  const cells = parseRow(line);
  if (!cells.length || isSeparatorRow(cells)) continue;

  const row = Object.fromEntries(headers.map((h, i) => [h, cells[i] ?? ""]));
  processedRows++;

  if (!row.work_id || !row.work_id.startsWith("RW-")) continue;
  if (row.status !== ACTIVE_STATUS) continue;
  activeRows++;

  if (!ALLOWED_CATEGORIES.has(row.category)) {
    issues.push(`Skipped ${row.work_id}: invalid category "${row.category}"`);
    continue;
  }

  const bmin = sanitizeNumber(row.budget_min_rub);
  const bmax = sanitizeNumber(row.budget_max_rub);
  const busmin = sanitizeNumber(row.business_min_rub);
  const busmax = sanitizeNumber(row.business_max_rub);
  const pmin = sanitizeNumber(row.premium_min_rub);
  const pmax = sanitizeNumber(row.premium_max_rub);

  if (![bmin, bmax, busmin, busmax, pmin, pmax].every(Number.isFinite)) {
    issues.push(`Skipped ${row.work_id}: invalid numeric values`);
    continue;
  }

  if (!(bmax < busmin && busmax < pmin && bmin <= bmax && busmin <= busmax && pmin <= pmax)) {
    issues.push(`Skipped ${row.work_id}: tier overlap detected`);
    continue;
  }

  records.push({
    work_id: row.work_id,
    category: row.category,
    work_name: row.work_name,
    unit: row.unit,
    budget_avg: Math.round((bmin + bmax) / 2),
    business_avg: Math.round((busmin + busmax) / 2),
    premium_avg: Math.round((pmin + pmax) / 2),
    material_norm: row.material_norm || "-",
    labor_hours: sanitizeNumber(row.labor_hours) || 0,
    source_count: sanitizeNumber(row.source_count) || 0,
    date_verified: row.date_verified
  });
}

if (!records.length) {
  dv.header(3, "Repair Price Matrix");
  dv.paragraph("No valid active pricing records available.");
  if (issues.length) {
    dv.header(4, "Validation Issues");
    dv.list(issues);
  }
  return;
}

// Group by category
const grouped = {};
for (const r of records) {
  if (!grouped[r.category]) grouped[r.category] = [];
  grouped[r.category].push(r);
}

// Render by category
dv.header(3, "Repair Price Matrix");
dv.paragraph(
  `Source: ${SOURCE_PATH} | Processed: ${processedRows} | Active: ${activeRows} | Categories: ${Object.keys(grouped).length}`
);

const categoryNames = {
  demolition: "🔨 Демонтаж",
  preparation: "🧱 Подготовка",
  walls: "🏗️ Стены",
  floors: "🪵 Полы",
  ceilings: "⬆️ Потолки",
  electrical: "⚡ Электрика",
  plumbing: "💧 Сантехника",
  finishing: "🎨 Отделка",
  cleaning: "🧹 Клининг"
};

for (const [cat, items] of Object.entries(grouped).sort()) {
  dv.header(4, categoryNames[cat] || cat);
  dv.table(
    ["Работа", "Ед.", "Budget (₽)", "Business (₽)", "Premium (₽)", "Материал", "Часы", "Источники", "Проверено"],
    items.map(r => [
      `${r.work_name} (${r.work_id})`,
      r.unit,
      r.budget_avg.toLocaleString("ru-RU"),
      r.business_avg.toLocaleString("ru-RU"),
      r.premium_avg.toLocaleString("ru-RU"),
      r.material_norm,
      r.labor_hours.toFixed(2),
      r.source_count,
      r.date_verified
    ])
  );
}

if (issues.length) {
  dv.header(4, "Validation Issues");
  dv.list(issues);
}
```

## Manual Fallback Table

| Категория | Работа | Ед. | Budget (₽) | Business (₽) | Premium (₽) | Материал | Часы |
|-----------|--------|-----|-----------:|-------------:|------------:|----------|------|
| demolition | Демонтаж перегородок | m2 |  |  |  |  |  |

## Export Protocol

1. Review dashboard output in Reading view
2. Resolve any entries listed in `Validation Issues`
3. Use Dataview block menu -> `Copy result`
4. Save exported snapshot under `08_Pricing_Tables/snapshots/repair/`
5. Recommended filename:
   - `repair_matrix_snapshot_YYYY-MM-DD.md`
   - `repair_matrix_snapshot_YYYY-MM-DD.csv`

## Governance Rules

- Do not export snapshots when validation issues affect active production rows
- Every active work in registry should preserve source traceability (>=2 sources)
- Keep `category` constrained to controlled vocabulary
- Re-verify prices every 30 days for `active` status
- Log all changes in `tier_rules_changelog.md`

## Evolution Path

Next recommended upgrade path:

1. Add cost breakdown (materials vs labor vs margin)
2. Support regional coefficients for geo scaling
3. Integrate with project estimates (`03_Renovation/projects/`)
4. Generate historical trend charts across snapshots
5. Auto-detect price anomalies using IQR method
6. Export to JSON API for external integrations
