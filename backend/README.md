# Backend

The current Phase 0 target backend layout is `backend/app/`.

Existing `backend/src/` and `backend/main.py` files are pre-existing
placeholders. Do not add Phase 0 feature logic there. Future implementation
phases should follow `docs/FOUNDATION.md` and `docs/STACK_AND_STRUCTURE.md`
before adding runnable backend behavior.

## Phase 1 test commands

After syncing backend dependencies, validate the core domain data model with:

```powershell
Set-Location backend
pytest tests/domain tests/repositories tests/migrations -q
```

The tests cover service rules, repository persistence behavior, model metadata,
and the Phase 1 Alembic revision surface. Phase 1 does not add public API
endpoints, CSV parsing, frontend runtime code, background jobs, or AI execution.

## Phase 2 test commands

After syncing Phase 2 backend dependencies, validate the CSV import pipeline
with:

```powershell
Set-Location backend
pytest tests/domain tests/repositories tests/api tests/workers -q
```

The Phase 2 suite covers CSV parsing and preview behavior, confirmed import
execution, status/history APIs, worker delegation, standard response envelopes,
pagination, and raw CSV non-retention.

## Phase 4 test commands

After syncing Phase 4 backend dependencies, validate the AI analysis engine with:

```powershell
Set-Location backend
pytest tests/domain tests/services tests/repositories tests/api tests/workers tests/migrations -q
```

The Phase 4 suite covers AI settings, daily/weekly input preparation, note-text
exclusion, output validation, idempotency, run history/current/rerun APIs,
retry/failure metadata, and thin Celery worker delegation.
