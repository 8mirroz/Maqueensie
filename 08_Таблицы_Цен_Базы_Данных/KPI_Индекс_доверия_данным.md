---
doc_id: confidence_index
doc_type: analytics_dashboard
version: 1.0.0
status: active
date_added: 2026-04-18
tags: [confidence, analytics, quality]
system_role: analytics_layer
responsibilities:
  - track_confidence_scores_across_records
  - surface_low_quality_data
  - enable_quality_based_filtering
interfaces:
  input:
    - source_folder: "07_Competitors/verified"
    - confidence_field: frontmatter.confidence_score
  output:
    - ranked_table_by_confidence
    - quality_distribution_summary
dependencies:
  - "scripts/analytics/compute_confidence.py"
  - "10_Guides/validation_rules.md"

title: "Индекс доверия данным"---

# Confidence Index

## SYSTEM BLOCK

| Attribute | Value |
|---|---|
| **System Role** | Analytics Layer + Quality Dashboard |
| **Primary Function** | Track and display confidence scores for all verified records |
| **Input Contract** | Frontmatter with `confidence_score` field from `07_Competitors/verified/` |
| **Output Contract** | Ranked table + quality distribution summary |
| **Update Frequency** | On-demand via `compute_confidence.py --update-frontmatter` |
| **Governance Owner** | Pricing Intelligence Governance Lead |

---

## CONFIDENCE SCORE METHODOLOGY

### Formula

```
confidence_score = 
    (source_quality × 0.3) + 
    (recency_factor × 0.25) + 
    (cross_validation × 0.25) + 
    (data_completeness × 0.2)
```

### Component Definitions

| Component | Weight | Calculation | Range |
|-----------|--------|-------------|-------|
| **Source Quality** | 30% | Based on URL domain classification | 0.3–1.0 |
| **Recency Factor** | 25% | `max(0, 1 - days_since_verification / 180)` | 0–1 |
| **Cross-Validation** | 25% | `min(1.0, source_count / 3) × 0.8` | 0–0.8 |
| **Data Completeness** | 20% | `filled_required_fields / total_required_fields` | 0–1 |

### Interpretation Scale

| Score Range | Label | Action |
|-------------|-------|--------|
| 0.8–1.0 | 🟢 High | Auto-Verified, priority for export |
| 0.6–0.8 | 🟡 Medium | Pending review, acceptable for dashboards |
| 0.4–0.6 | 🟠 Low | Warning, requires data enrichment |
| 0.0–0.4 | 🔴 Critical | Reject or archive, do not use in analysis |

---

## DYNAMIC CONFIDENCE TABLE (DataviewJS)

```dataviewjs
// ============================================================
// CONFIDENCE INDEX DASHBOARD v1.0.0
// Displays records ranked by confidence score
// ============================================================

const CONFIG = {
  sourceFolder: "07_Competitors/verified",
  minConfidence: 0.0, // Show all; set to 0.6 for "Medium+" only
};

// Helper: extract first value from array or return as-is
function unwrap(value) {
  if (Array.isArray(value) && value.length > 0) return value[0];
  if (Array.isArray(value) && value.length === 0) return "";
  return value || "";
}

// Helper: get confidence label
function getConfidenceLabel(score) {
  if (score >= 0.8) return { label: "High", icon: "🟢" };
  if (score >= 0.6) return { label: "Medium", icon: "🟡" };
  if (score >= 0.4) return { label: "Low", icon: "🟠" };
  return { label: "Critical", icon: "🔴" };
}

// Main processing
const pages = dv.pages(`"${CONFIG.sourceFolder}"`)
  .filter(p => {
    const score = p.confidence_score ?? 0;
    return score >= CONFIG.minConfidence;
  })
  .sort((a, b) => {
    const scoreA = a.confidence_score ?? 0;
    const scoreB = b.confidence_score ?? 0;
    return scoreB - scoreA; // Descending
  });

if (pages.length === 0) {
  dv.paragraph("⚠️ **Нет записей с confidence_score**. Запустите `python scripts/analytics/compute_confidence.py --update-frontmatter`");
} else {
  const records = pages.map(p => {
    const score = p.confidence_score ?? 0;
    const { label, icon } = getConfidenceLabel(score);
    return {
      competitor: unwrap(p.competitor),
      domain: unwrap(p.domain),
      tier: unwrap(p.price_tier),
      score: score.toFixed(3),
      label: `${icon} ${label}`,
      date_verified: p.date_verified || "—",
      sources: Array.isArray(p.source_urls) ? p.source_urls.length : 0,
      file_link: p.file.link
    };
  });

  dv.table(
    ["Конкурент", "Домен", "Tier", "Score", "Уровень", "Дата верификации", "Источников"],
    records.map(r => [
      r.file_link,
      r.domain,
      r.tier,
      r.score,
      r.label,
      r.date_verified,
      r.sources
    ])
  );

  // Summary statistics
  const scores = pages.map(p => p.confidence_score ?? 0);
  const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
  const highCount = scores.filter(s => s >= 0.8).length;
  const mediumCount = scores.filter(s => s >= 0.6 && s < 0.8).length;
  const lowCount = scores.filter(s => s >= 0.4 && s < 0.6).length;
  const criticalCount = scores.filter(s => s < 0.4).length;

  dv.paragraph("---");
  dv.paragraph("**Статистика качества данных**");
  dv.paragraph([
    `📊 Всего записей: **${scores.length}**`,
    `📈 Средний score: **${avgScore.toFixed(3)}**`,
    `🟢 High (≥0.8): **${highCount}** (${(highCount/scores.length*100).toFixed(1)}%)`,
    `🟡 Medium (0.6-0.8): **${mediumCount}** (${(mediumCount/scores.length*100).toFixed(1)}%)`,
    `🟠 Low (0.4-0.6): **${lowCount}** (${(lowCount/scores.length*100).toFixed(1)}%)`,
    `🔴 Critical (<0.4): **${criticalCount}** (${(criticalCount/scores.length*100).toFixed(1)}%)`
  ].join("\n"));
}
```

---

## UPDATE PROTOCOL

### Ручное обновление

```bash
# Вычислить scores и обновить frontmatter
python scripts/analytics/compute_confidence.py --update-frontmatter

# Только просмотр статистики
python scripts/analytics/compute_confidence.py
```

### Автоматическое обновление (Future)

Интегрировать в CI/CD пайплайн:
- Запуск при каждом коммите в `07_Competitors/verified/`
- Блокировка merge если средний score < 0.6

---

## GOVERNANCE RULES

### Минимальные требования для экспорта

| Экспорт | Min Confidence | Примечание |
|---------|----------------|------------|
| Внутренний дашборд | 0.4 (Low+) | С предупреждением |
| Еженедельный отчёт | 0.6 (Medium+) | Стандартное качество |
| Внешний API | 0.8 (High) | Только проверенные данные |

### Эскалация проблем

- **>20% записей с Critical**: остановить экспорт, запустить аудит данных
- **Средний score < 0.6**: пересмотреть источники, обновить validation rules
- **Отдельная запись упала с High до Critical**: уведомить Data Steward

---

## EVOLUTION PLAN

### v1.0 → v2.0

- [ ] Добавить тренды confidence во времени
- [ ] Интеграция с anomaly detection
- [ ] Автоматические рекомендации по улучшению score

### v2.0 → v3.0

- [ ] Машинное обучение для классификации источников
- [ ] Прогнозирование устаревания данных
- [ ] Интеграция с внешними системами мониторинга

---

*Документ версия: 1.0.0*  
*Дата создания: 2026-04-18*  
*Владелец: Pricing Intelligence Governance Lead*
