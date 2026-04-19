# План развития репозитория: Архитектура, Алгоритмы и Автоматизация

## Executive Summary

Данный документ определяет стратегический план развития репозитория Obsidian Knowledge OS от текущей версии (v2.0) до production-grade системы уровня v3.0+. 

**Текущее состояние:**
- ✅ Базовая архитектура с MOC-структурой реализована
- ✅ DataviewJS дашборды с валидацией работают
- ✅ Политики валидации определены (`10_Guides/validation_rules.md`)
- ✅ Python-скрипты для валидации существуют
- ❌ Папка `07_Competitors/` пуста — нет данных для анализа
- ❌ Нет автоматического сбора данных
- ❌ Нет исторических снимков (snapshots)
- ❌ Нет CI/CD пайплайна
- ❌ Нет системы оценки достоверности (confidence scoring)

**Целевое состояние (v3.0):**
- Автоматический сбор данных из внешних источников
- Историческая аналитика трендов цен
- Confidence scoring для каждой записи
- CI/CD валидация при каждом коммите
- JSON API для экспорта во внешние системы

---

## 1. АРХИТЕКТУРНОЕ РАЗВИТИЕ

### 1.1 Многослойная архитектура данных

```
┌─────────────────────────────────────────────────────────────┐
│                    DECISION LAYER                           │
│  - Dashboards (DataviewJS)                                  │
│  - Analytics Reports                                        │
│  - Export/API Gateway                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓ reads from
┌─────────────────────────────────────────────────────────────┐
│                   ANALYTICS LAYER                           │
│  - Trend Tracker (historical)                               │
│  - Price Overlap Detection                                  │
│  - Confidence Scoring Engine                                │
└─────────────────────────────────────────────────────────────┘
                            ↓ reads from
┌─────────────────────────────────────────────────────────────┐
│               STANDARDIZED LAYER                            │
│  - Normalized competitor profiles                           │
│  - Validated price ranges                                   │
│  - Controlled vocabulary enforced                           │
└─────────────────────────────────────────────────────────────┘
                            ↓ reads from
┌─────────────────────────────────────────────────────────────┐
│                  RAW INGEST LAYER                           │
│  - External scrapers output                                 │
│  - Manual entry buffers                                     │
│  - API ingestion logs                                       │
└─────────────────────────────────────────────────────────────┘
```

**Новые компоненты для создания:**

| Слой | Компонент | Путь | Статус |
|------|-----------|------|--------|
| Raw Ingest | Scraper output buffer | `07_Competitors/_ingest/` | ❌ Требуется |
| Raw Ingest | Ingestion log | `07_Competitors/_logs/ingestion_YYYY-MM-DD.md` | ❌ Требуется |
| Standardized | Validated profiles | `07_Competitors/verified/` | ❌ Требуется |
| Analytics | Historical snapshots | `08_Pricing_Tables/snapshots/` | ❌ Требуется |
| Analytics | Confidence index | `08_Pricing_Tables/confidence_index.md` | ❌ Требуется |
| Decision | Export API spec | `config/api/export_schema.json` | ❌ Требуется |

### 1.2 Расширение структуры каталогов

```bash
/workspace
├── 07_Competitors/
│   ├── _ingest/              # Новые: буфер сырых данных
│   │   └── raw_YYYY-MM-DD_HHMMSS_source.json
│   ├── _logs/                # Новые: логи импорта
│   │   └── ingestion_YYYY-MM-DD.md
│   ├── verified/             # Новые: прошедшие валидацию
│   │   └── YYYY-MM-DD_Competitor_Service.md
│   └── rejected/             # Новые: отклонённые валидацией
│       └── rejection_log_YYYY-MM-DD.md
├── 08_Pricing_Tables/
│   ├── snapshots/            # Новые: исторические снимки
│   │   └── competitor_snapshot_YYYY-MM-DD_vX.X.X.md
│   ├── exports/              # Новые: CSV/JSON экспорты
│   │   └── competitor_export_YYYY-MM-DD.csv
│   └── confidence_index.md   # Новый: индекс доверия
├── config/
│   ├── api/                  # Новый: спецификации API
│   │   ├── export_schema.json
│   │   └── rate_limits.yaml
│   └── scrapers/             # Новый: конфиги скраперов
│       ├── architecture_sites.yaml
│       └── interior_sites.yaml
└── scripts/
    ├── ingest/               # Новые: скрипты импорта
    │   ├── scraper_runner.py
    │   ├── validate_ingest.py
    │   └── promote_to_verified.py
    ├── analytics/            # Новые: аналитика
    │   ├── compute_confidence.py
    │   ├── detect_anomalies.py
    │   └── generate_snapshots.py
    └── ci_cd/                # Новые: CI/CD хуки
        ├── pre_commit_check.py
        └── github_actions_validator.py
```

### 1.3 Data Contracts (Контракты данных)

**Входящий контракт (Raw Ingest → Standardized):**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["competitor", "domain", "service_type", "price_raw", "source_url", "scrape_timestamp"],
  "properties": {
    "competitor": {"type": "string"},
    "domain": {"type": "string", "enum": ["Architecture", "Interior", "Renovation", "Decor", "Furniture", "RealEstate"]},
    "service_type": {"type": "string"},
    "price_raw": {
      "type": "object",
      "required": ["value", "currency", "unit"],
      "properties": {
        "value": {"type": "number", "minimum": 0},
        "currency": {"type": "string", "default": "RUB"},
        "unit": {"type": "string", "enum": ["m2", "package", "hour"]}
      }
    },
    "source_url": {"type": "string", "format": "uri"},
    "scrape_timestamp": {"type": "string", "format": "date-time"},
    "metadata": {"type": "object"}
  }
}
```

**Исходящий контракт (Standardized → Analytics):**

См. `10_Guides/validation_rules.md` — требуется расширить версионированием схемы.

---

## 2. АЛГОРИТМИЧЕСКОЕ РАЗВИТИЕ

### 2.1 Нормализация цен

**Проблема:** Источники используют разные валюты, единицы измерения и форматы.

**Алгоритм нормализации:**

```python
def normalize_price(raw_price, source_currency, source_unit, target_currency="RUB", target_unit="m2"):
    """
    Нормализует цену к целевой валюте и единице измерения.
    
    Args:
        raw_price: числовое значение
        source_currency: валюта источника (USD, EUR, RUB)
        source_unit: единица измерения источника (m2, package, hour)
        target_currency: целевая валюта (по умолчанию RUB)
        target_unit: целевая единица (по умолчанию m2)
    
    Returns:
        dict: {value_rub_m2: float, confidence: float, conversion_chain: list}
    """
    # Шаг 1: Конвертация валюты
    rate = get_exchange_rate(source_currency, target_currency)  # Из кэша или API
    price_in_target_currency = raw_price * rate
    
    # Шаг 2: Конвертация единиц
    if source_unit == "package" and target_unit == "m2":
        # Требуется оценка площади из контекста
        estimated_area = estimate_area_from_context(metadata)  # 50-250 m2 по умолчанию
        price_per_m2 = price_in_target_currency / estimated_area
        confidence = 0.6  # Снижаем доверие из-за оценки
    elif source_unit == "hour" and target_unit == "m2":
        # Требуется оценка трудоёмкости
        hours_per_m2 = 0.5  # По умолчанию
        price_per_m2 = price_in_target_currency * hours_per_m2
        confidence = 0.5
    else:
        price_per_m2 = price_in_target_currency
        confidence = 0.9
    
    return {
        "value_rub_m2": round(price_per_m2, 2),
        "confidence": confidence,
        "conversion_chain": [f"{raw_price} {source_currency}/{source_unit}", f"× {rate}", f"= {price_per_m2} {target_currency}/{target_unit}"]
    }
```

**Внедрение:** Создать `scripts/analytics/normalize_prices.py`

### 2.2 Confidence Scoring (Оценка достоверности)

**Формула расчёта:**

```
confidence_score = 
    (source_quality × 0.3) + 
    (recency_factor × 0.25) + 
    (cross_validation × 0.25) + 
    (data_completeness × 0.2)

где:
- source_quality: 0.3–1.0 (официальный сайт=1.0, агрегатор=0.7, форум=0.3)
- recency_factor: max(0, 1 - days_since_verification / 180)
- cross_validation: min(1.0, verified_sources_count / 3) × 0.8
- data_completeness: filled_required_fields / total_required_fields
```

**Шкала интерпретации:**

| Score | Уровень | Действие |
|-------|---------|----------|
| 0.8–1.0 | High | Автоматически Verified, зелёная метка |
| 0.6–0.8 | Medium | Pending, требует ручной проверки |
| 0.4–0.6 | Low | Warning, показать в диагностике |
| 0.0–0.4 | Critical | Отклонить или пометить Outdated |

**Внедрение:** 
1. Добавить поле `confidence_score` в frontmatter
2. Создать `scripts/analytics/compute_confidence.py`
3. Обновить DataviewJS для отображения score в таблице

### 2.3 Детекция аномалий

**Алгоритм:**

```python
def detect_price_anomalies(records, domain, tier):
    """
    Обнаруживает выбросы в ценах для данного домена и тира.
    
    Метод: IQR (Interquartile Range)
    """
    prices = [r["price_range_rub"][0] for r in records if r["domain"] == domain and r["price_tier"] == tier]
    
    if len(prices) < 5:
        return []  # Недостаточно данных
    
    q1 = percentile(prices, 25)
    q3 = percentile(prices, 75)
    iqr = q3 - q1
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    anomalies = []
    for r in records:
        if r["domain"] != domain or r["price_tier"] != tier:
            continue
        price = r["price_range_rub"][0]
        if price < lower_bound or price > upper_bound:
            anomalies.append({
                "competitor": r["competitor"],
                "price": price,
                "reason": "below_lower_bound" if price < lower_bound else "above_upper_bound",
                "bounds": [lower_bound, upper_bound],
                "deviation_percent": abs(price - median(prices)) / median(prices) * 100
            })
    
    return anomalies
```

**Внедрение:** 
- Создать `scripts/analytics/detect_anomalies.py`
- Добавить секцию "Аномалии" в `02_Competitor_Comparison_Dashboard.md`

### 2.4 Кросс-валидация с Tier Rules

**Логика:**

```python
def validate_against_tier_rules(record, tier_rules):
    """
    Проверяет соответствие записи правилам tier_rules.md
    
    Returns:
        dict: {valid: bool, violations: list, suggestions: list}
    """
    violations = []
    suggestions = []
    
    rule = find_matching_rule(tier_rules, record["domain"], record["service_type"])
    if not rule:
        return {"valid": True, "violations": [], "suggestions": ["No matching tier rule found"]}
    
    price_min, price_max = record["price_range_rub"]
    tier = record["price_tier"]
    
    if tier == "Budget_Ready":
        if price_min < rule["budget_min_rub"]:
            violations.append(f"Price below budget_min_rub ({rule['budget_min_rub']})")
        if price_max > rule["budget_max_rub"]:
            suggestions.append(f"Consider adjusting max to {rule['budget_max_rub']} for Budget tier")
    
    elif tier == "Business":
        if price_min < rule["business_min_rub"]:
            violations.append(f"Price below business_min_rub ({rule['business_min_rub']})")
        if price_max > rule["business_max_rub"]:
            violations.append(f"Price exceeds business_max_rub ({rule['business_max_rub']})")
    
    elif tier == "Premium_Ultra":
        if price_min < rule["premium_min_rub"]:
            violations.append(f"Price below premium_min_rub ({rule['premium_min_rub']})")
    
    return {
        "valid": len(violations) == 0,
        "violations": violations,
        "suggestions": suggestions
    }
```

---

## 3. АВТОМАТИЗАЦИЯ ОБНОВЛЕНИЯ ДАННЫХ

### 3.1 Внешние скраперы (Python/Node.js)

**Архитектура скрапера:**

```python
# scripts/ingest/scraper_runner.py
import asyncio
import aiohttp
from pathlib import Path
import json
from datetime import datetime

SOURCES_CONFIG = {
    "architecture": [
        {"name": "archi.ru", "url": "https://archi.ru/projects", "selector": ".price-card"},
        {"name": "houzz.ru", "url": "https://houzz.ru/professionals", "selector": ".pricing-info"},
    ],
    "interior": [
        {"name": "inmyroom.ru", "url": "https://inmyroom.ru/designers", "selector": ".service-price"},
    ]
}

async def scrape_source(session, source_config):
    async with session.get(source_config["url"]) as response:
        html = await response.text()
        # Парсинг через BeautifulSoup или lxml
        extracted_data = parse_html(html, source_config["selector"])
        return {
            "source": source_config["name"],
            "timestamp": datetime.utcnow().isoformat(),
            "data": extracted_data
        }

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for category, sources in SOURCES_CONFIG.items():
            for source in sources:
                tasks.append(scrape_source(session, source))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Сохранение в буфер
        ingest_dir = Path("07_Competitors/_ingest")
        ingest_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_file = ingest_dir / f"raw_{timestamp}.json"
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"Ingested {len(results)} sources → {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
```

**План внедрения:**
1. Неделя 1: Базовый скрапер для 2-3 источников
2. Неделя 2: Валидация сырых данных
3. Неделя 3: Интеграция с promotion pipeline

### 3.2 CI/CD пайплайн (GitHub Actions)

**Файл `.github/workflows/validate_kb.yml`:**

```yaml
name: Validate Knowledge Base

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pyyaml jsonschema
    
    - name: Run structure validation
      run: python scripts/validate_kb.py
    
    - name: Run data contract validation
      run: python scripts/ingest/validate_ingest.py
    
    - name: Check for stale data (>30 days)
      run: python scripts/analytics/check_freshness.py
    
    - name: Generate diagnostics report
      run: python scripts/analytics/generate_diagnostics.py --output diagnostics_report.json
    
    - name: Upload diagnostics artifact
      uses: actions/upload-artifact@v3
      with:
        name: kb-diagnostics
        path: diagnostics_report.json
    
    - name: Fail on critical errors
      run: |
        if jq -e '.critical_errors > 0' diagnostics_report.json; then
          echo "Critical errors detected!"
          exit 1
        fi
```

**Дополнительные workflow:**

```yaml
# .github/workflows/snapshot_export.yml
name: Weekly Snapshot Export

on:
  schedule:
    - cron: '0 0 * * 0'  # Каждое воскресенье в 00:00

jobs:
  export:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Generate snapshot
      run: python scripts/analytics/generate_snapshots.py
    
    - name: Commit snapshot
      run: |
        git config --local user.name "GitHub Actions Bot"
        git config --local user.email "actions@github.com"
        git add 08_Pricing_Tables/snapshots/
        git commit -m "Auto: weekly snapshot $(date +%Y-%m-%d)" || echo "No changes"
        git push
```

### 3.3 Система снапшотов и истории

**Скрипт генерации снимков:**

```python
# scripts/analytics/generate_snapshots.py
import json
from pathlib import Path
from datetime import datetime
import hashlib

def generate_snapshot():
    """Создаёт снимок текущего состояния базы конкурентов."""
    
    competitors_dir = Path("07_Competitors/verified")
    snapshot_dir = Path("08_Pricing_Tables/snapshots")
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    # Сбор всех валидированных записей
    records = []
    for md_file in competitors_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)
        records.append({
            "file": md_file.name,
            "competitor": frontmatter.get("competitor"),
            "domain": frontmatter.get("domain"),
            "price_range_rub": frontmatter.get("price_range_rub"),
            "date_verified": frontmatter.get("date_verified"),
            "status": frontmatter.get("status"),
            "confidence_score": frontmatter.get("confidence_score", 0.0)
        })
    
    # Метаданные снимка
    snapshot_metadata = {
        "timestamp": datetime.utcnow().isoformat(),
        "record_count": len(records),
        "domains": list(set(r["domain"] for r in records if r["domain"])),
        "sha256": hashlib.sha256(json.dumps(records).encode()).hexdigest()
    }
    
    # Сохранение JSON
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    json_file = snapshot_dir / f"snapshot_{timestamp}.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump({"metadata": snapshot_metadata, "records": records}, f, indent=2)
    
    # Создание Markdown-отчёта
    md_report = f"""---
doc_id: snapshot_{timestamp}
doc_type: historical_snapshot
snapshot_date: {timestamp}
record_count: {len(records)}
---

# Snapshot Report: {timestamp}

## Summary

- **Total Records**: {len(records)}
- **Domains**: {', '.join(snapshot_metadata['domains'])}
- **SHA256**: `{snapshot_metadata['sha256']}`

## Changes Since Last Snapshot

*Требуется сравнение с предыдущим снимком*

## Raw Data

См. `{json_file.name}`
"""
    
    md_file = snapshot_dir / f"snapshot_{timestamp}.md"
    md_file.write_text(md_report, encoding="utf-8")
    
    print(f"Snapshot created: {md_file}")
    return md_file
```

---

## 4. ДОРОЖНАЯ КАРТА ВНЕДРЕНИЯ

### Фаза 1: Foundation (Недели 1-2)

| Задача | Приоритет | Оценка (ч) | Статус |
|--------|-----------|------------|--------|
| Создать структуру `_ingest/`, `verified/`, `rejected/` | P0 | 1 | ❌ |
| Реализовать базовый скрапер для 2 источников | P0 | 8 | ❌ |
| Настроить GitHub Actions для валидации | P0 | 4 | ❌ |
| Добавить поле `confidence_score` в шаблоны | P1 | 2 | ❌ |

### Фаза 2: Analytics Engine (Недели 3-4)

| Задача | Приоритет | Оценка (ч) | Статус |
|--------|-----------|------------|--------|
| Реализовать нормализацию цен | P0 | 6 | ❌ |
| Внедрить confidence scoring алгоритм | P0 | 8 | ❌ |
| Создать детектор аномалий | P1 | 6 | ❌ |
| Интегрировать кросс-валидацию с tier_rules | P1 | 8 | ❌ |

### Фаза 3: Automation (Недели 5-6)

| Задача | Приоритет | Оценка (ч) | Статус |
|--------|-----------|------------|--------|
| Настроить еженедельные снапшоты | P0 | 4 | ❌ |
| Расширить скрапер на 5+ источников | P1 | 12 | ❌ |
| Создать dashboard для мониторинга качества | P1 | 8 | ❌ |
| Реализовать auto-promotion из ingest → verified | P2 | 10 | ❌ |

### Фаза 4: Advanced Features (Недели 7-8)

| Задача | Приоритет | Оценка (ч) | Статус |
|--------|-----------|------------|--------|
| Историческая аналитика трендов | P1 | 16 | ❌ |
| JSON API для экспорта данных | P2 | 12 | ❌ |
| Визуализация графиков распределения цен | P2 | 10 | ❌ |
| Интеграция с внешними BI-системами | P3 | 20 | ❌ |

---

## 5. RISK MANAGEMENT

| Риск | Вероятность | Влияние | Митигация |
|------|-------------|---------|-----------|
| Скраперы ломаются из-за изменений вёрстки сайтов | Высокая | Среднее | Абстрактный парсер-адаптер, мониторинг ошибок |
| Ложные срабатывания детектора аномалий | Средняя | Низкое | Ручная калибровка порогов, whitelist исключений |
| Переполнение хранилища снапшотами | Низкая | Низкое | Политика ротации: хранить последние 12 снимков |
| CI/CD слишком медленный (>10 мин) | Средняя | Среднее | Кэширование зависимостей, параллелизация задач |
| Конфликты слияния при частых обновлениях | Средняя | Высокое | Feature branches, обязательные PR review |

---

## 6. GOVERNANCE & COMPLIANCE

### 6.1 Контроль качества данных

**Quality Gates перед продвижением в `verified/`:**

1. ✅ Все required fields заполнены
2. ✅ `confidence_score >= 0.6`
3. ✅ Минимум 1 источник URL
4. ✅ `date_verified` не старше 30 дней
5. ✅ Проходит кросс-валидацию с tier_rules (или помечено как exception)

### 6.2 Роли и ответственность

| Роль | Обязанности | Доступ |
|------|-------------|--------|
| Data Steward | Ручная проверка Pending записей | Write to `verified/` |
| Governance Lead | Обновление tier_rules, политик | Admin access |
| System Bot | Авто-скрапинг, валидация, снапшоты | Write to `_ingest/`, `snapshots/` |
| Analyst | Чтение, экспорт, аналитика | Read-only |

### 6.3 Аудит и трассируемость

Каждое изменение должно быть запротоколировано:

```markdown
## Changelog Entry Template

- **Дата**: YYYY-MM-DD
- **Автор**: @username или @system-bot
- **Тип**: [Ingest | Validation | Promotion | Correction | Deprecation]
- **Затронутые файлы**: [...]
- **Обоснование**: ...
- **Evidence**: [URL, screenshot, hash]
```

---

## 7. ЗАКЛЮЧЕНИЕ

Предложенный план трансформирует репозиторий из статичной коллекции заметок в динамическую производственную систему с:

- ✅ Автоматическим сбором данных
- ✅ Многоуровневой валидацией
- ✅ Исторической аналитикой
- ✅ Прозрачным качеством данных (confidence scoring)
- ✅ CI/CD гарантиями

**Следующие шаги:**
1. Утвердить дорожную карту
2. Начать с Фазы 1 (Foundation)
3. Еженедельно пересматривать прогресс

---

*Документ версия: 1.0.0*  
*Дата создания: 2026-04-18*  
*Владелец: Pricing Intelligence Governance Lead*
