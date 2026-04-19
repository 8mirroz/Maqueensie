# Конфигурация источников для скрапинга

## Architecture

- **archi.ru**
  - URL: https://archi.ru/projects
  - Selector: `.price-card`
  - Update frequency: weekly
  - Priority: high

- **houzz.ru**
  - URL: https://houzz.ru/professionals
  - Selector: `.pricing-info`
  - Update frequency: weekly
  - Priority: high

## Interior

- **inmyroom.ru**
  - URL: https://inmyroom.ru/designers
  - Selector: `.service-price`
  - Update frequency: weekly
  - Priority: medium

- **ivd.ru**
  - URL: https://ivd.ru/studio
  - Selector: `.price-block`
  - Update frequency: biweekly
  - Priority: medium

## Renovation

- **remontnik.ru**
  - URL: https://remontnik.ru/prices
  - Selector: `.price-item`
  - Update frequency: daily
  - Priority: high

## Notes

- Все источники должны поддерживать rate limiting (1 запрос в 2 секунды)
- Требуется ротация User-Agent при частых запросах
- Кэширование ответов на 24 часа минимум
