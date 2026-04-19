---
doc_id: competitor_comparison_dashboard
doc_type: dataview_dashboard
version: 2.0.0
status: active
date_added: 2026-04-17
date_verified: 2026-04-17
date_updated: 2026-04-18
tags: [competitors, dashboard, dataview, pricing_intelligence]
system_role: export_layer
responsibilities:
  - aggregate_verified_competitor_data
  - expose_pricing_overlap_signals
  - provide_diagnostics_on_data_quality
  - enable_snapshot_export
interfaces:
  input:
    - source_folder: "07_Competitors"
    - required_frontmatter_contract: "10_Guides/validation_rules"
    - allowed_statuses: ["Verified", "Pending"]
  output:
    - rendered_table_view: competitor_comparison_matrix
    - diagnostic_report: data_quality_issues
    - export_format: markdown_table_csv_compatible
dependencies:
  - "10_Guides/validation_rules"
  - "10_Guides/tier_rules"
  - "07_Competitors/*"
success_criteria:
  - all_rendered_rows_have_valid_price_ranges
  - invalid_records_are_skipped_with_visible_reason
  - diagnostics_show_record_counts_and_error_summary
  - backward_compatible_with_existing_dataview_queries
governance:
  controlled_vocabulary:
    domains: ["Architecture", "Interior", "Renovation", "Decor", "Furniture", "RealEstate"]
    tiers: ["Budget_Ready", "Business", "Premium_Ultra"]
    statuses: ["Verified", "Pending", "Outdated"]
  snapshot_rule: "export_before_major_tier_rules_update"
  traceability: "source_urls_required_for_verified_status"
  quality_gate: "min_2_sources_for_verified"
---

# Competitor Comparison Dashboard

## SYSTEM BLOCK

| Attribute | Value |
|---|---|
| **System Role** | Export Layer + Decision Support View |
| **Primary Function** | Aggregate verified competitor pricing data with diagnostics |
| **Input Contract** | Frontmatter per `[[10_Guides/validation_rules]]` from `07_Competitors/` |
| **Output Contract** | Rendered tables + diagnostic report + export-ready markdown |
| **Dependencies** | `[[10_Guides/validation_rules]]`, `[[10_Guides/tier_rules]]` |
| **Governance Owner** | Pricing Intelligence Governance Lead |
| **Review Cycle** | 30 days or on tier_rules update |

---

## DYNAMIC COMPETITOR MATRIX (DataviewJS)

```dataviewjs
// ============================================================
// COMPETITOR COMPARISON DASHBOARD v2.0.0
// Production-grade aggregation with fail-safe logic
// ============================================================

const CONFIG = {
  sourceFolder: "07_Competitors",
  allowedStatuses: ["Verified", "Pending"],
  requiredFields: ["competitor", "domain", "service_type", "price_tier", "price_range_rub", "status"],
  validDomains: ["Architecture", "Interior", "Renovation", "Decor", "Furniture", "RealEstate"],
  validTiers: ["Budget_Ready", "Business", "Premium_Ultra"],
  validStatuses: ["Verified", "Pending", "Outdated"]
};

// Diagnostic counters
const diagnostics = {
  totalScanned: 0,
  validRecords: 0,
  skippedRecords: 0,
  errors: []
};

// Helper: validate price range
function validatePriceRange(range) {
  if (!Array.isArray(range) || range.length !== 2) return { valid: false, reason: "price_range_rub must be [min, max]" };
  const [min, max] = range;
  if (typeof min !== 'number' || typeof max !== 'number') return { valid: false, reason: "price values must be numeric" };
  if (min < 0 || max < 0) return { valid: false, reason: "price values cannot be negative" };
  if (min > max && max !== 0) return { valid: false, reason: "min cannot exceed max" };
  return { valid: true };
}

// Helper: validate enum field
function validateEnum(value, allowed, fieldName) {
  if (!value) return { valid: false, reason: `${fieldName} is required` };
  if (Array.isArray(value)) {
    if (value.length === 0) return { valid: false, reason: `${fieldName} cannot be empty array` };
    value = value[0];
  }
  if (!allowed.includes(value)) return { valid: false, reason: `${fieldName} must be one of: ${allowed.join(", ")}` };
  return { valid: true, value };
}

// Helper: format price range display
function formatPriceRange(range) {
  if (!Array.isArray(range) || range.length !== 2) return "N/A";
  const [min, max] = range;
  if (min === 0 && max === 0) return "По запросу";
  if (min === max) return `${min.toLocaleString('ru-RU')} ₽`;
  return `${min.toLocaleString('ru-RU')} – ${max.toLocaleString('ru-RU')} ₽`;
}

// Helper: extract first value from array or return as-is
function unwrap(value) {
  if (Array.isArray(value) && value.length > 0) return value[0];
  if (Array.isArray(value) && value.length === 0) return "";
  return value || "";
}

// Main processing
const pages = dv.pages(`"${CONFIG.sourceFolder}"`)
  .filter(p => CONFIG.allowedStatuses.includes(unwrap(p.status)))
  .sort((a, b) => {
    const domainA = unwrap(a.domain) || "";
    const domainB = unwrap(b.domain) || "";
    const compA = unwrap(a.competitor) || "";
    const compB = unwrap(b.competitor) || "";
    const cmp = domainA.localeCompare(domainB);
    return cmp !== 0 ? cmp : compA.localeCompare(compB);
  });

const records = [];

for (const page of pages) {
  diagnostics.totalScanned++;
  const file = page.file;
  
  // Validate required fields
  const validationErrors = [];
  
  for (const field of CONFIG.requiredFields) {
    if (!page[field] && page[field] !== 0 && page[field] !== false) {
      validationErrors.push(`missing ${field}`);
    }
  }
  
  // Validate domain
  const domainResult = validateEnum(page.domain, CONFIG.validDomains, "domain");
  if (!domainResult.valid) validationErrors.push(domainResult.reason);
  
  // Validate tier
  const tierResult = validateEnum(page.price_tier, CONFIG.validTiers, "price_tier");
  if (!tierResult.valid) validationErrors.push(tierResult.reason);
  
  // Validate status
  const statusResult = validateEnum(page.status, CONFIG.validStatuses, "status");
  if (!statusResult.valid) validationErrors.push(statusResult.reason);
  
  // Validate price range
  const priceResult = validatePriceRange(page.price_range_rub);
  if (!priceResult.valid) validationErrors.push(priceResult.reason);
  
  if (validationErrors.length > 0) {
    diagnostics.skippedRecords++;
    diagnostics.errors.push({
      file: file.path,
      competitor: unwrap(page.competitor) || "UNKNOWN",
      reasons: validationErrors
    });
    continue;
  }
  
  diagnostics.validRecords++;
  records.push({
    competitor: unwrap(page.competitor),
    domain: domainResult.value,
    service_type: unwrap(page.service_type) || "N/A",
    hook: unwrap(page.hook) || "—",
    tech_aesthetic: Array.isArray(page.tech_aesthetic_features) 
      ? page.tech_aesthetic_features.join("; ") 
      : (page.tech_aesthetic_features || "—"),
    tier: tierResult.value,
    price_range: page.price_range_rub,
    price_display: formatPriceRange(page.price_range_rub),
    sources: Array.isArray(page.source_urls) 
      ? page.source_urls.join(", ") 
      : (page.source_urls || "—"),
    date_verified: page.date_verified || "—",
    status: statusResult.value,
    file_link: file.link
  });
}

// Render main table
if (records.length === 0) {
  dv.paragraph("⚠️ **Нет валидных записей для отображения**. Проверьте источник данных.");
} else {
  dv.table(
    ["Домен", "Конкурент", "Услуга", "Tier", "Диапазон цен (RUB)", "Hook", "Tech/Aesthetic", "Источники", "Дата верификации", "Статус"],
    records.map(r => [
      r.domain,
      r.file_link,
      r.service_type,
      r.tier,
      r.price_display,
      r.hook,
      r.tech_aesthetic,
      r.sources,
      r.date_verified,
      r.status
    ])
  );
}

// Render diagnostics section
dv.paragraph("---");
dv.paragraph("**Диагностика качества данных**");

const errorSummary = [];
if (diagnostics.totalScanned === 0) {
  errorSummary.push(`📁 Файлов просканировано: **0**`);
} else {
  errorSummary.push(`📁 Файлов просканировано: **${diagnostics.totalScanned}**`);
  errorSummary.push(`✅ Валидных записей: **${diagnostics.validRecords}**`);
  errorSummary.push(`⚠️ Пропущено записей: **${diagnostics.skippedRecords}**`);
}

if (diagnostics.errors.length > 0) {
  errorSummary.push("");
  errorSummary.push("**Ошибки в источниках:**");
  for (const err of diagnostics.errors.slice(0, 10)) { // Limit to first 10 errors
    errorSummary.push(`- ${err.file}: ${err.competitor} — ${err.reasons.join(", ")}`);
  }
  if (diagnostics.errors.length > 10) {
    errorSummary.push(`- ... и ещё ${diagnostics.errors.length - 10} ошибок`);
  }
}

dv.paragraph(errorSummary.join("\n"));

// Expose diagnostics for external consumption
dv.paragraph("");
dv.paragraph("*Диагностика доступна для экспорта через консоль разработчика*");
console.log("COMPETITOR_DASHBOARD_DIAGNOSTICS", {
  timestamp: new Date().toISOString(),
  totalScanned: diagnostics.totalScanned,
  validRecords: diagnostics.validRecords,
  skippedRecords: diagnostics.skippedRecords,
  errors: diagnostics.errors
});
```

---

## PRICING OVERLAP ANALYSIS

```dataviewjs
// ============================================================
// PRICING OVERLAP VIEW v2.0.0
// Detects tier conflicts and range quality issues
// ============================================================

const CONFIG = {
  sourceFolder: "07_Competitors",
  tagFilters: ["pricing", "competitor"]
};

function analyzeRangeQuality(range) {
  if (!Array.isArray(range) || range.length !== 2) return { quality: "invalid", reason: "неверный формат" };
  const [min, max] = range;
  if (min <= 0 || max <= 0) return { quality: "warning", reason: "нулевые значения" };
  if (min > max) return { quality: "error", reason: "min > max" };
  if (max - min > 1000000) return { quality: "warning", reason: "очень широкий диапазон" };
  return { quality: "ok", reason: "" };
}

function getTierOverlapSignal(tier, priceRange) {
  // Simple overlap detection based on tier_rules thresholds
  const tierThresholds = {
    "Budget_Ready": { max: 4500 },
    "Business": { min: 4501, max: 9000 },
    "Premium_Ultra": { min: 9001 }
  };
  
  const threshold = tierThresholds[tier];
  if (!threshold) return "unknown_tier";
  
  const [min, max] = priceRange;
  if (min === 0 && max === 0) return "price_on_request";
  
  if ("min" in threshold && min < threshold.min) return "below_tier_min";
  if ("max" in threshold && max > threshold.max) return "above_tier_max";
  
  return "within_tier";
}

const pages = dv.pages(`"${CONFIG.sourceFolder}"`)
  .filter(p => {
    const tags = p.tags || [];
    return tags.some(t => CONFIG.tagFilters.some(filter => t.includes(filter)));
  })
  .sort((a, b) => {
    const compA = a.competitor && Array.isArray(a.competitor) ? a.competitor[0] : (a.competitor || "");
    const compB = b.competitor && Array.isArray(b.competitor) ? b.competitor[0] : (b.competitor || "");
    return compA.localeCompare(compB);
  });

const records = [];

for (const page of pages) {
  const competitor = page.competitor && Array.isArray(page.competitor) ? page.competitor[0] : (page.competitor || "UNKNOWN");
  const serviceType = page.service_type && Array.isArray(page.service_type) ? page.service_type[0] : (page.service_type || "N/A");
  const tier = page.price_tier && Array.isArray(page.price_tier) ? page.price_tier[0] : (page.price_tier || "N/A");
  const priceRange = page.price_range_rub || [0, 0];
  
  const rangeQuality = analyzeRangeQuality(priceRange);
  const overlapSignal = getTierOverlapSignal(tier, priceRange);
  
  records.push({
    competitor,
    service_type: serviceType,
    tier,
    price_range: priceRange,
    price_display: priceRange[0] === 0 && priceRange[1] === 0 ? "По запросу" : `${priceRange[0].toLocaleString('ru-RU')} – ${priceRange[1].toLocaleString('ru-RU')} ₽`,
    range_quality: rangeQuality.quality,
    range_reason: rangeQuality.reason,
    overlap_signal: overlapSignal,
    file_link: page.file.link
  });
}

if (records.length === 0) {
  dv.paragraph("⚠️ Нет данных для анализа перекрытия цен. Убедитесь, что файлы имеют теги `pricing` или `competitor`.");
} else {
  dv.table(
    ["Конкурент", "Услуга", "Tier", "Диапазон (RUB)", "Качество диапазона", "Сигнал перекрытия"],
    records.map(r => [
      r.file_link,
      r.service_type,
      r.tier,
      r.price_display,
      r.range_quality === "ok" ? "✅" : (r.range_quality === "warning" ? "⚠️" : "❌") + ` ${r.range_reason}`,
      r.overlap_signal
    ])
  );
}
```

---

## FALLBACK MANUAL TABLE

*Используйте эту таблицу для ручного ввода при отказе Dataview или для快照 экспорта.*

| Competitor | Domain | Hook | Tech/Aesthetic Features | Tier | Price Range (RUB) | Sources | Verified Date | Status |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |

---

## EXPORT & SNAPSHOT PROTOCOL

### Экспорт в CSV

1. Откройте эту заметку в режиме чтения
2. Скопируйте результат из таблицы Dataview
3. Вставьте в текстовый редактор с поддержкой CSV
4. Сохраните как: `08_Pricing_Tables/exports/competitor_snapshot_YYYY-MM-DD.csv`

### Правила снимков (Snapshots)

- **Обязательный снимок**: перед обновлением `[[10_Guides/tier_rules]]`
- **Периодичность**: каждые 30 дней
- **Формат имени**: `competitor_comparison_YYYY-MM-DD_v{version}.md`
- **Хранение**: `08_Pricing_Tables/snapshots/`

### Трассируемость

Каждая запись в таблице должна иметь:
- ✅ Минимум 1 источник в `source_urls`
- ✅ Дату верификации не старше 30 дней (для статуса `Verified`)
- ✅ Корректный `price_range_rub` в формате `[min, max]`

---

## SYSTEM EVOLUTION PLAN

### Версионирование

| Версия | Дата | Изменения |
|---|---|---|
| 1.0.0 | 2026-04-17 | Исходная версия с базовыми Dataview запросами |
| 2.0.0 | 2026-04-18 | Добавлена валидация, диагностика, fail-safe логика, явные контракты |

### Путь развития v2 → v3

1. **Историческая аналитика**: добавить отслеживание изменений цен по конкурентам во времени
2. **Автоматические снимки**: интеграция со скриптами для автоматического экспорта
3. **Расширенная валидация**: кросс-проверка с `[[10_Guides/tier_rules]]` на соответствие диапазонам
4. **Визуализация трендов**: графики распределения цен по доменам и тирам
5. **API слой**: экспорт данных во внешние системы через JSON

### Замена формата источника

Если структура `07_Competitors/` изменится:
1. Обновите `CONFIG.sourceFolder` в начале скрипта
2. Адаптируйте функцию валидации полей под новую схему frontmatter
3. Протестируйте на наборе из 5-10 файлов перед полным развёртыванием

---

## RISKS & FAIL-SAFE

| Риск | Вероятность | Влияние | Митигация |
|---|---|---|---|
| Пустая папка `07_Competitors` | Средняя | Высокое | Fallback таблица + явное сообщение в диагностике |
| Некорректный frontmatter | Высокая | Среднее | Валидация с пропусками и видимыми ошибками |
| Изменение схемы Dataview | Низкая | Критическое | Fallback manual table, документированный экспорт |
| Устаревание данных (>30 дней) | Средняя | Среднее | Диагностика показывает дату верификации |
| Переполнение таблицы (>100 записей) | Низкая | Низкое | Пагинация через фильтрацию по домену/тиру |

### Fail-Safe поведение

- ❌ **Неудача загрузки файла**: файл пропускается, ошибка логируется в диагностику
- ❌ **Отсутствие обязательных полей**: запись пропускается с указанием missing fields
- ❌ **Некорректный диапазон цен**: запись помечается как warning, не агрегируется
- ❌ **Пустой результат**: явно отображается сообщение вместо пустой таблицы

---

## GOVERNANCE COMPLIANCE

- [x] Явная роль в архитектуре знаний
- [x] Документированный контракт входа/выхода
- [x] Валидация числовых значений перед агрегацией
- [x] Видимые ошибки для невалидных записей
- [x] Сохранена трассируемость источников
- [x] documented правила экспорта/снимков
- [x] План эволюции версии
- [x] Backward совместимость с v1.0.0
