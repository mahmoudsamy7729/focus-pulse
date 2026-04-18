# Analytics Module

Owns read-only dashboard aggregation for Phase 3.

## Boundaries

- Routers expose versioned read endpoints and return standard success envelopes.
- Services resolve day/week/month periods, latest tracked day fallback, empty states, summary totals, timelines, category grouping, and tag notices.
- Repositories own SQLAlchemy reads against active `DailyLog`, `Task`, and `Category` records.
- This module does not write dashboard tables, mutate tracking data, enqueue jobs, run AI insight generation, export reports, or synchronize with Notion.

## Endpoint

- `GET /api/v1/analytics/dashboard`

Required scope: `analytics:read`.
