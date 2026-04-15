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
