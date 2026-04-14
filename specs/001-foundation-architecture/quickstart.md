# Quickstart: Validate Phase 0 Foundation & Architecture

Use this quickstart after `/speckit.tasks` and implementation to verify that Phase 0 stayed within its skeleton-only boundary.

## 1. Confirm Feature Context

```powershell
git branch --show-current
Get-Content .specify\feature.json
```

Expected:

- Branch is `001-foundation-architecture`.
- Feature directory is `specs/001-foundation-architecture`.

## 2. Review Planning Artifacts

Check these files:

- `specs/001-foundation-architecture/spec.md`
- `specs/001-foundation-architecture/plan.md`
- `specs/001-foundation-architecture/research.md`
- `specs/001-foundation-architecture/data-model.md`
- `specs/001-foundation-architecture/contracts/foundation-package.md`
- `specs/001-foundation-architecture/quickstart.md`

Expected:

- No unresolved clarification markers.
- No Phase 1+ implementation requirements.
- No runtime API contract.

## 3. Validate Foundation Documentation

Check:

- `docs/FOUNDATION.md`
- `docs/STACK_AND_STRUCTURE.md`
- `docs/Plan.md`

Expected:

- Product purpose is clear.
- v1 scope boundaries are clear.
- Naming conventions are explicit.
- Practical v1 baselines are documented.
- AI can read validated productivity data and write separate insights, but cannot mutate source logs, tasks, or imports.

## 4. Validate Skeleton Paths

Inspect expected skeleton areas:

```powershell
Get-ChildItem backend\app -Recurse -Depth 3
Get-ChildItem frontend -Recurse -Depth 3
Get-ChildItem docker -Recurse -Depth 3
```

Expected:

- Backend module folders use snake_case.
- Frontend product feature folders use kebab-case where product-facing.
- Placeholder files contain only explanatory content.
- No domain behavior appears in skeleton files.

## 5. Validate Forbidden Outputs Are Absent

Search for evidence of out-of-scope Phase 0 implementation:

```powershell
rg -n "APIRouter|create_async_engine|declarative_base|Celery\\(|pandas|csv|prompt|agent|useQuery|axios" backend frontend specs docs
```

Expected:

- Matches in docs/specs are acceptable when describing future architecture.
- Matches in Phase 0 skeleton source files should be absent unless they are placeholder comments.
- No CSV import, dashboard, database schema, worker task, or AI behavior exists.

## 6. Classify Future Work

Use the foundation package to classify proposed tasks:

- In scope: skeleton folders, placeholder docs, env examples, compose placeholders, architecture notes.
- Out of scope: runnable apps, APIs, schemas, imports, dashboards, AI runs, CI gates.
- Amendment required: any Phase 0 change that alters stack, naming, AI boundary, or v1 scope.

## Next Step

After this plan is accepted, run `/speckit.tasks` to generate the implementation task list for Phase 0.
