# Quickstart: CSV Import Pipeline

Use this quickstart to validate the Phase 2 plan artifacts and later implementation output.

## 1. Confirm Active Feature

```powershell
git branch --show-current
Get-Content .specify\feature.json
```

Expected:

- Branch is `003-csv-import-pipeline`.
- `.specify/feature.json` points to `specs/003-csv-import-pipeline`.

## 2. Review Planning Artifacts

```powershell
Get-Content specs\003-csv-import-pipeline\spec.md
Get-Content specs\003-csv-import-pipeline\plan.md
Get-Content specs\003-csv-import-pipeline\research.md
Get-Content specs\003-csv-import-pipeline\data-model.md
Get-Content specs\003-csv-import-pipeline\contracts\import-api.yaml
```

Expected:

- No `NEEDS CLARIFICATION` markers remain.
- The plan stays inside Phase 2 CSV import scope.
- Dashboard visualization, AI execution, scheduled imports, Notion API sync, and report export are explicitly out of scope.

## 3. Validate Intended Backend Ownership

```powershell
Get-ChildItem backend\app\modules\imports
Get-ChildItem backend\app\modules\imports\services
Get-ChildItem backend\app\modules\imports\repositories
Get-ChildItem backend\app\workers
```

Expected after implementation:

- CSV parsing, preview, import execution, exceptions, schemas, router, and dependencies live in `backend\app\modules\imports`.
- Celery app and thin import task live in `backend\app\workers`.
- Daily log, task, category, and note persistence still flows through the existing domain services.
- No Phase 2 feature logic is added to root `backend\main.py` or `backend\src\main.py`.

## 4. Validate CSV Preview Behavior

Use a CSV file with:

```csv
date,task,category,time_spent_minutes,tags,notes
2026-04-15, Write Plan , Deep Work , 45, writing, useful note
April 15, 2026,Write Plan,Deep Work,45,writing,duplicate
,Missing Date,Admin,10,,
```

Expected preview behavior:

- The first two rows parse as valid row candidates.
- Date parsing accepts both `2026-04-15` and `April 15, 2026`.
- Tags split on commas, lowercase, trim, and de-duplicate.
- Empty notes become `null`.
- The missing-date row is invalid with a row-specific reason.
- No `ImportRun`, `DailyLog`, `Task`, `Category`, `Note`, or `ImportRowOutcome` record is created by preview.

## 5. Validate Confirmed Import Behavior

After implementation exposes `/api/v1/imports/csv`, submit the same CSV for confirmed import.

Expected:

- Response status is `202`.
- JSON success response uses `{ "success": true, "data": ... }`.
- Response includes `import_run_id` and initial status `pending`.
- A background import task processes the normalized payload.
- The existing DailyLog is reused for repeated dates.
- Duplicate row identity is date + normalized task name + time spent.
- Duplicate rows are skipped and recorded as row outcomes.
- Invalid rows are recorded as row outcomes.
- Full raw CSV contents are not retained in import history.

## 6. Validate Status and History APIs

After implementation, inspect:

```text
GET /api/v1/imports/{import_run_id}
GET /api/v1/imports/{import_run_id}/row-outcomes?page=1&limit=20
GET /api/v1/imports?page=1&limit=20
```

Expected:

- All handled JSON responses use the standard success envelope.
- Handled errors use the unified error schema with stable error codes.
- ImportRun status uses only `pending`, `processing`, `completed`, `completed_with_errors`, or `failed`.
- Row counts match inserted, invalid, skipped, and failed outcomes.
- List endpoints use `page` and `limit` with a maximum limit of 100.

## 7. Validate Tests

After implementation defines Phase 2 code, run:

```powershell
Set-Location backend
pytest tests/domain tests/repositories tests/api tests/workers -q
```

Expected:

- Parser tests cover required columns, optional columns, empty files, unreadable CSV, ISO dates, Notion-style dates, invalid dates, duration validation, comma-separated tags, duplicate tags, empty tags, and empty notes.
- Preview tests prove no ImportRun or tracking records are created.
- Import service tests cover successful inserts, invalid rows, duplicate rows, row outcomes, terminal statuses, and raw CSV non-retention.
- API tests verify success and error envelopes, status codes, scopes, rate-limit behavior or dependency hooks, and pagination contracts.
- Worker tests verify the Celery task delegates to services and does not duplicate business rules.

## 8. Confirm Out-of-Scope Surfaces

```powershell
rg -n "AIInsight|prompt|scheduled|notion api|report export|chart|dashboard" backend frontend specs\003-csv-import-pipeline
```

Expected:

- Matches inside `specs\003-csv-import-pipeline` are acceptable when documenting out-of-scope work.
- Phase 2 implementation should not add AI execution, scheduled import behavior, Notion API synchronization, dashboard visualization, or report export.
