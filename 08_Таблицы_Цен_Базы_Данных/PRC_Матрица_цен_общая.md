---
doc_id: price_matrix
doc_type: dataview_dashboard
status: active
date_added: 2026-04-17
date_verified: 2026-04-17
tags: [pricing, matrix, dataview]

title: "Матрица цен общая"---

# Price Matrix — Domain × Tier

## Dataview Plugin Setup

1. Obsidian Settings -> Community plugins -> install `Dataview`.
2. Enable `JavaScript Queries` in Dataview settings.
3. Open this note in Reading view.

## Dynamic Matrix (from `10_Guides/tier_rules.md`)

```dataviewjs
const raw = await dv.io.load("10_Guides/tier_rules.md");
const lines = raw.split("\n").filter(l => l.trim().startsWith("|"));
if (lines.length < 3) {
  dv.paragraph("No tier rules table found.");
} else {
  const parseRow = (line) => line.split("|").slice(1, -1).map(v => v.trim());
  const headers = parseRow(lines[0]);
  const records = [];

  for (const line of lines.slice(2)) {
    const cells = parseRow(line);
    if (!cells.length || !cells[0].startsWith("TR-")) continue;
    const row = Object.fromEntries(headers.map((h, i) => [h, cells[i] ?? ""]));
    if (row.status !== "active") continue;

    const tiers = [
      ["Economy", Number(row.economy_min_rub), Number(row.economy_max_rub)],
      ["Comfort", Number(row.comfort_min_rub), Number(row.comfort_max_rub)],
      ["Business", Number(row.business_min_rub), Number(row.business_max_rub)],
      ["Premium", Number(row.premium_min_rub), Number(row.premium_max_rub || row.premium_min_rub)],
    ];

    for (const [tier, minV, maxV] of tiers) {
      if (!Number.isFinite(minV) || !Number.isFinite(maxV)) continue;
      records.push({
        domain: row.domain,
        metric_type: row.metric_type,
        tier,
        min: minV,
        max: maxV,
        avg: (minV + maxV) / 2,
        sources: row.source_urls,
      });
    }
  }

  const grouped = {};
  for (const r of records) {
    const k = `${r.domain}|${r.metric_type}|${r.tier}`;
    grouped[k] ||= [];
    grouped[k].push(r);
  }

  const result = Object.entries(grouped).map(([k, items]) => {
    const [domain, metric_type, tier] = k.split("|");
    const mins = items.map(i => i.min);
    const maxs = items.map(i => i.max);
    const avgs = items.map(i => i.avg);
    return {
      domain,
      metric_type,
      tier,
      min_rub: Math.min(...mins),
      max_rub: Math.max(...maxs),
      avg_rub: Math.round(avgs.reduce((a, b) => a + b, 0) / avgs.length),
      source_urls: [...new Set(items.map(i => i.sources).filter(Boolean))].join("; "),
    };
  }).sort((a, b) => (a.domain + a.tier).localeCompare(b.domain + b.tier));

  dv.table(
    ["Domain", "Metric", "Tier", "Min (RUB)", "Max (RUB)", "Avg (RUB)", "Source URLs"],
    result.map(r => [r.domain, r.metric_type, r.tier, r.min_rub, r.max_rub, r.avg_rub, r.source_urls])
  );
}
```

## Fallback Manual Table

| Domain | Metric | Tier | Min (RUB) | Max (RUB) | Avg (RUB) | Source URLs |
|---|---|---|---:|---:|---:|---|
| Architecture | rub_m2 | Budget_Ready |  |  |  |  |

## Export to CSV/Markdown

1. Dataview block menu -> `Copy result` -> paste into CSV/MD editor.
2. Save exported table under `08_Pricing_Tables/` with date suffix for snapshots.
