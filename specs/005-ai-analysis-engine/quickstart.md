# Quickstart: AI Analysis Engine

This quickstart validates the Phase 4 planning artifacts and defines the expected implementation smoke checks for `/speckit.tasks` and later implementation.

## Planning Artifact Review

From the repository root:

```powershell
Get-ChildItem specs\005-ai-analysis-engine
Get-ChildItem specs\005-ai-analysis-engine\contracts
```

Expected artifacts:

- `specs/005-ai-analysis-engine/spec.md`
- `specs/005-ai-analysis-engine/plan.md`
- `specs/005-ai-analysis-engine/research.md`
- `specs/005-ai-analysis-engine/data-model.md`
- `specs/005-ai-analysis-engine/contracts/ai-insights-api.yaml`
- `specs/005-ai-analysis-engine/quickstart.md`

Review these checks before task generation:

- Phase 4 is limited to basic AI analysis runs.
- No Phase 5 productivity score, consistency score, best/worst day, or recommendation behavior is planned.
- No Phase 6 scheduled AI run behavior is planned.
- Note text is excluded from AI inputs and generated outputs.
- Full structured AI input payloads are not retained after source references and aggregate summaries are recorded.
- Analysis run statuses use the shared vocabulary: `pending`, `processing`, `completed`, `completed_with_errors`, `failed`.
- No-data analysis requests complete with output outcome `no_data`.
- Transient failures stop after no more than 3 total attempts.

## Contract Review

Open the API contract:

```powershell
Get-Content specs\005-ai-analysis-engine\contracts\ai-insights-api.yaml
```

Confirm:

- All endpoints live under `/api/v1`.
- JSON success responses use `success: true` and `data`.
- Handled errors use `success: false` and `error.code`.
- Run history uses `page` and `limit`.
- Write endpoints require `ai_insights:write`.
- Read endpoints require `ai_insights:read`.
- Write/rerun endpoints document stricter rate limits than reads.

## Expected Backend Implementation Checks

After Phase 4 implementation tasks are completed, run from `backend/`:

```powershell
pytest tests/domain tests/services tests/repositories tests/api tests/workers tests/migrations -q
```

Expected coverage:

- Daily and weekly period validation.
- Privacy-bounded input preparation excluding note text.
- Aggregate input summary retention without full input payload retention.
- Combined output validation for required sections and evidence references.
- No-data output with status `completed` and output outcome `no_data`.
- Retry limit of 3 total attempts and final `failed` status after exhausted retries.
- Rerun creation preserves previous run history.
- Idempotency key behavior and in-flight conflict handling.
- API success/error envelope shape, auth scopes, pagination, rate-limit metadata, and not-found/conflict mappings.
- Worker task delegates to AI analysis services without duplicating business rules.
- Migration adds Phase 4 AI run metadata without mutating source tracking tables.

## Manual Smoke Flow After Implementation

Use existing Phase 1-3 test data helpers or create saved tracking records through lower-level services.

1. Create saved daily tracking records for one day with tasks, categories, tags, durations, and optional notes.
2. Request daily AI analysis:

   ```http
   POST /api/v1/ai-insights/runs
   Idempotency-Key: daily-2026-04-15

   {
     "period_granularity": "daily",
     "anchor_date": "2026-04-15"
   }
   ```

3. Confirm the response status is `202`, response body is wrapped in the success envelope, and the run starts as `pending`.
4. Process the worker task using the deterministic test provider or eager Celery mode.
5. Fetch the run:

   ```http
   GET /api/v1/ai-insights/runs/{ai_insight_run_id}
   ```

6. Confirm:

   - Status is `completed`.
   - Output outcome is `analysis_generated`.
   - Output has summary, detected patterns, behavior insights, supporting evidence, limitations, and generated timestamp.
   - Supporting evidence references dates, task counts, categories, tags, durations, or task references.
   - No note text appears in source summary or output.

7. Request a period with no saved tracking records.
8. Confirm the run status is `completed` and output outcome is `no_data`.
9. Trigger a transient provider failure with the fake provider.
10. Confirm no more than 3 total attempts occur and final failure details are traceable if all attempts fail.

## Out-of-Scope Checks

Verify Phase 4 implementation does not add:

- CSV import behavior.
- Dashboard visualization changes.
- Productivity or consistency scores.
- Best/worst day labels.
- Recommendations.
- Scheduled AI runs.
- AI chat.
- Report export.
- Notion API synchronization.
