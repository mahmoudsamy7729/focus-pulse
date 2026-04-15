# Quickstart: Core Domain & Data Model

Use this quickstart to validate the Phase 1 plan artifacts and later implementation output.

## 1. Confirm Active Feature

```powershell
git branch --show-current
Get-Content .specify\feature.json
```

Expected:

- Branch is `002-core-domain-data-model`.
- `.specify/feature.json` points to `specs/002-core-domain-data-model`.

## 2. Review Planning Artifacts

```powershell
Get-Content specs\002-core-domain-data-model\spec.md
Get-Content specs\002-core-domain-data-model\plan.md
Get-Content specs\002-core-domain-data-model\research.md
Get-Content specs\002-core-domain-data-model\data-model.md
Get-Content specs\002-core-domain-data-model\contracts\domain-data-contract.md
```

Expected:

- No `NEEDS CLARIFICATION` markers remain.
- The plan stays inside Phase 1 domain/data-model scope.
- CSV upload, dashboard UI, AI execution, scheduling, and production hardening are explicitly out of scope.

## 3. Validate Intended Backend Ownership

```powershell
Get-ChildItem backend\app\modules\daily_logs
Get-ChildItem backend\app\modules\tasks
Get-ChildItem backend\app\modules\notes
Get-ChildItem backend\app\modules\imports
Get-ChildItem backend\app\modules\ai_insights
```

Expected after implementation:

- Domain models live in their owning modules.
- Services live under module `services/` folders.
- Repositories live under module `repositories/` folders.
- No Phase 1 feature logic is added to `backend\src\main.py` or root `backend\main.py`.

## 4. Validate Model Rules

Review implementation against these checks:

- `DailyLog` is unique by owner and calendar date.
- New data for an existing date reuses the existing `DailyLog`.
- `Task` belongs to exactly one `DailyLog`.
- `Task.time_spent_minutes` is a positive whole number.
- `Category` is normalized and reused by canonical name.
- `Task.tags` is a JSON array of unique lowercase trimmed values.
- Empty tags become `[]`.
- Empty notes do not create a Note.
- Import duplicate rows are skipped by date + normalized task name + time spent.
- Import row outcomes exist for invalid, skipped, and failed rows.
- ImportRun and AIInsightRun share statuses: `pending`, `processing`, `completed`, `completed_with_errors`, `failed`.
- AIInsightRun supports daily and weekly target periods only.

## 5. Validate Migration and Tests

After implementation defines test tooling, run the Phase 1 backend tests from the command documented by tasks, expected to be similar to:

```powershell
Set-Location backend
pytest tests/domain tests/repositories tests/migrations -q
```

Expected:

- Service tests cover normalization, uniqueness, deduplication, run status transitions, and target-period validation.
- Repository tests cover active-record filtering and traceability reads.
- Migration tests or manual migration review confirm all Phase 1 tables, indexes, constraints, and relationships exist.

## 6. Confirm Out-of-Scope Surfaces

```powershell
rg -n "upload|parse csv|Celery\(|prompt|agent|useQuery|axios|page.tsx|route.ts" backend frontend specs\002-core-domain-data-model
```

Expected:

- Matches inside `specs/002-core-domain-data-model` are acceptable when documenting deferred work.
- Phase 1 implementation should not add CSV upload/parsing flow, Celery jobs, AI prompt execution, dashboard pages, or frontend data fetching.
