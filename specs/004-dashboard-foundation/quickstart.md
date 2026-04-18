# Quickstart: Dashboard Foundation

This quickstart validates the Phase 3 planning artifacts and defines the expected validation path for implementation.

## 1. Verify Planning Artifacts

From the repository root:

```powershell
Get-Content .specify\feature.json
Get-ChildItem specs\004-dashboard-foundation
Get-ChildItem specs\004-dashboard-foundation\contracts
```

Expected:

- `.specify/feature.json` points to `specs/004-dashboard-foundation`.
- `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, and `contracts/dashboard-api.yaml` exist.
- The plan states Phase 3 is read-only and excludes imports, editing, AI, automation, reports, and Notion API sync.

## 2. Review API Contract

Open:

```powershell
Get-Content specs\004-dashboard-foundation\contracts\dashboard-api.yaml
```

Confirm:

- All endpoints are under `/api/v1`.
- Dashboard overview uses `GET /analytics/dashboard`.
- Day detail uses `GET /daily-logs/{log_date}`.
- Success responses use `{ success: true, data: ... }`.
- Error responses use `{ success: false, error: { code, message, details } }`.
- Read endpoints define scopes and rate-limit expectations.

## 3. Review Data Rules

Open:

```powershell
Get-Content specs\004-dashboard-foundation\data-model.md
```

Confirm:

- Dashboard defaults to the latest tracked day when data exists.
- Day/week/month period rules are explicit.
- Category and tag charts use top 10 plus `Other`.
- Untagged tasks are represented in tag breakdowns.
- Multi-tag counting is documented.
- Day detail task order uses source/import order with saved order fallback.

## 4. Expected Backend Validation After Implementation

After Phase 3 tasks are implemented:

```powershell
Set-Location backend
pytest tests/api tests/services tests/repositories -q
```

Minimum backend checks:

- Dashboard endpoint returns the standard success envelope.
- Day detail endpoint returns the standard success envelope.
- Invalid period filters return unified error responses.
- Read scopes are enforced.
- Soft-deleted records are excluded.
- Category totals reconcile to total tracked time.
- Tag breakdown includes `untagged` and multi-tag notice behavior.
- Top 10 plus `Other` grouping preserves chart totals.

## 5. Expected Frontend Validation After Implementation

After the frontend package is bootstrapped:

```powershell
Set-Location frontend
npm install
npm run lint
npm run build
```

Minimum frontend checks:

- `/dashboard` renders the dashboard as the primary experience.
- The dashboard defaults to the latest tracked day returned by the API.
- Day, week, and month filters update the query and visible data.
- Summary cards display hours-and-minutes values.
- Week/month views show daily totals timeline data.
- Day detail shows the day-focused task timeline.
- Empty states render for no data and no selected-period data.

## 6. Manual End-to-End Smoke Check

With backend, database, and frontend running after implementation:

1. Import a small CSV using the Phase 2 flow.
2. Open the dashboard.
3. Confirm it starts on the latest tracked day.
4. Switch to week and month filters.
5. Open a day detail row.
6. Confirm category and tag charts remain readable when more than 10 labels exist.

No AI insight, report export, scheduling, data editing, or Notion API behavior should be required for this phase.
