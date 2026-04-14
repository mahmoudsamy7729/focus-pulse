# FocusPulse

FocusPulse is a personal productivity system planned with Spec Kit. Phase 0 is
the foundation package only: it records the product purpose, v1 boundaries,
architecture rules, naming conventions, and skeleton repository layout for
future phases.

## Phase 0 Validation

Phase 0 has no required test, lint, type-check, or dev-server command. Validate
the current foundation package by following:

- `specs/001-foundation-architecture/quickstart.md`
- `docs/FOUNDATION.md`
- `docs/Plan.md`
- `docs/STACK_AND_STRUCTURE.md`

Useful manual checks from the quickstart:

```powershell
git branch --show-current
Get-Content .specify\feature.json
Get-ChildItem backend\app -Recurse -Depth 3
Get-ChildItem frontend -Recurse -Depth 3
Get-ChildItem docker -Recurse -Depth 3
rg -n "APIRouter|create_async_engine|declarative_base|Celery\(|pandas|csv|prompt|agent|useQuery|axios" backend frontend specs docs
```

Matches in planning documents are acceptable when they describe future
architecture. Phase 0 skeleton files must remain explanatory and must not add
runnable backend, frontend, database, worker, import, dashboard, or AI behavior.

## Repository Pointers

- `docs/FOUNDATION.md`: Phase 0 foundation package and review checklist.
- `docs/Plan.md`: phase-by-phase product plan.
- `docs/STACK_AND_STRUCTURE.md`: target stack and module layout.
- `backend/app/`: future FastAPI application target layout.
- `frontend/`: future Next.js dashboard target layout.
- `docker/`: future Docker support files.
