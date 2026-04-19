# Interior Knowledge Map (Moscow)

> [!NOTE]
> Данный раздел содержит структурированную базу знаний по рынку интерьеров Москвы, включая коммерческие и жилые сегменты. Информация используется для формирования офферов и анализа конкурентов.

## 📊 Market Intelligence
Аналитические отчеты, воронки продаж и маркетинговые хуки.

> [!TIP]
> См. также: [[residential-interiors__moscow-mo__moc__research_index|MOC — жилые интерьеры (Москва/МО)]]

```dataview
TABLE type AS Type, domain AS Domain, market AS Market
FROM "02_Interior"
WHERE type = "intelligence_report" OR type = "strategy_analysis" OR type = "offers_library"
SORT created DESC
```

## 💰 Pricing & Competition
Матрицы цен и сравнительный анализ игроков рынка.

```dataview
TABLE type AS Type, market AS Market, tags AS Tags
FROM "02_Interior"
WHERE type = "pricing_table" OR type = "competitor_matrix"
SORT created DESC
```

## 🛠 Tech Stack & Tools
Инструменты лидеров и технологические "билды".

```dataview
TABLE domain AS Domain, tags AS Tags
FROM "02_Interior/04_Tech_Stack"
```

## 🧠 Elite Strategy & Patterns (Strategic)
> Паттерны лидеров индустрии (Gensler, SOM, Officenext).

```dataview
TABLE region as "Region", tags as "Focus"
FROM "02_Interior/06_Strategy_and_Guides"
```

## 🏆 Best Cases & Award Winners
> Библиотека лучших реализаций 2025-2026 (РФ и Мир).

```dataview
TABLE type as "Type", region as "Region"
FROM "02_Interior/05_Best_Cases"
```

## 🛋 Furniture & Complectation (New Expansion)
> Сорсинг, цены и маркетинговые механики для мебели и декора.
> См. также: [[Furniture_MOC|MOC — Мебель и Декор]]

```dataview
TABLE type as "Type", tags as "Tags"
FROM "03_Furniture"
WHERE type != "moc"
SORT type ASC
```

## 📂 All Notes
```dataview
LIST FROM "02_Interior" WHERE file.name != this.file.name
```

