# Quickstart: Automation & Reliability

This quickstart validates the Phase 6 plan and later implementation without expanding scope beyond backend automation, scheduled imports, scheduled AI analysis, retries, logs, auditability, and run history.

## Planning Validation

1. Confirm the feature branch:

   ```powershell
   git branch --show-current
   ```

   Expected: `007-automation-reliability`.

2. Review the specification and plan:

   ```powershell
   Get-Content specs\007-automation-reliability\spec.md
   Get-Content specs\007-automation-reliability\plan.md
   ```

   Expected: Phase 6 is limited to backend automation APIs, scheduled imports, scheduled AI analysis runs, retry/recovery behavior, logs, auditability, and automation status/history.

3. Review generated design artifacts:

   ```powershell
   Get-Content specs\007-automation-reliability\research.md
   Get-Content specs\007-automation-reliability\data-model.md
   Get-Content specs\007-automation-reliability\contracts\automation-api.yaml
   ```

   Expected: No unresolved clarification markers and no planned frontend schedule-management UI.

## Backend Implementation Smoke Checks

Run after implementation tasks are complete.

1. Apply migrations:

   ```powershell
   Set-Location backend
   alembic upgrade head
   ```

2. Run targeted backend tests:

   ```powershell
   Set-Location backend
   pytest tests/domain tests/services tests/repositories tests/api tests/workers tests/migrations -q
   ```

3. Run the full backend suite:

   ```powershell
   Set-Location backend
   pytest -q
   ```

## API Behavior Checks

Use an authenticated owner with `imports:*` and `ai_insights:*` scopes in seeded test data.

1. Create a scheduled import:

   ```http
   POST /api/v1/imports/schedules
   Authorization: Bearer <token>
   Content-Type: application/json

   {
     "cadence": "daily",
     "local_run_time": "06:00",
     "timezone": "Africa/Cairo",
     "source_name": "daily-focuspulse-csv",
     "source_reference": {
       "kind": "configured_csv_reference",
       "reference_id": "csv-source-1"
     }
   }
   ```

   Expected: `201` success envelope with an active schedule, next run time, and no raw CSV contents.

2. Trigger the import schedule:

   ```http
   POST /api/v1/imports/schedules/{schedule_id}/trigger
   Authorization: Bearer <token>
   Idempotency-Key: import-window-2026-04-21
   ```

   Expected: `202` success envelope with a scheduled import run. Repeating the same trigger returns the existing run or a handled conflict without duplicate import records.

3. Fetch scheduled import history:

   ```http
   GET /api/v1/imports/schedules/{schedule_id}/runs?page=1&limit=20
   Authorization: Bearer <token>
   ```

   Expected: page/limit pagination, status, outcome, attempt count, linked ImportRun when started, row-count summary when available, and no raw CSV contents.

4. Create a scheduled AI analysis:

   ```http
   POST /api/v1/ai-insights/analysis-schedules
   Authorization: Bearer <token>
   Content-Type: application/json

   {
     "target_period_type": "weekly",
     "cadence": "weekly",
     "local_run_time": "07:00",
     "timezone": "Africa/Cairo"
   }
   ```

   Expected: `201` success envelope with an active schedule using `last_completed_week` period rule.

5. Trigger the AI analysis schedule:

   ```http
   POST /api/v1/ai-insights/analysis-schedules/{schedule_id}/trigger
   Authorization: Bearer <token>
   Idempotency-Key: ai-week-2026-04-13
   ```

   Expected: `202` success envelope with a scheduled AI analysis run linked to an `AIInsightRun` when started. No Phase 5 `AIInsightResult` is generated automatically.

6. Fetch scheduled AI analysis history:

   ```http
   GET /api/v1/ai-insights/analysis-schedules/{schedule_id}/runs?page=1&limit=20
   Authorization: Bearer <token>
   ```

   Expected: page/limit pagination, target period, status, outcome, attempt count, linked AIInsightRun when started, output outcome when available, and failure details when applicable.

## Worker Behavior Checks

1. Run due schedule evaluation in test/eager mode.

   Expected:

   - Only active schedules are evaluated.
   - Duplicate evaluator calls create zero duplicate schedule-run records.
   - After simulated downtime, only the latest missed window is processed and older missed windows are recorded as skipped.

2. Force retryable failures.

   Expected:

   - Scheduled runs retry up to three total attempts.
   - All attempts are traceable.
   - Exhausted retry attempts end in `failed`.

3. Force non-retryable failures.

   Expected:

   - Runs fail without repeated automatic retries.
   - Failure details are user-actionable.

4. Verify retention behavior.

   Expected:

   - Detailed history and audit detail remain available for 90 days.
   - Pruned older diagnostics preserve final summaries.

## Out-of-Scope Guardrails

The implementation must not add:

- Frontend schedule-management UI.
- Automatic Phase 5 insight generation.
- Report export.
- Notion API synchronization.
- AI chat.
- Dashboard redesign.
- Arbitrary external import connectors.
- Raw CSV retention.
- New AI recommendation logic.
