# Quickstart: Insights & Recommendations

This quickstart validates the Phase 5 plan and later implementation without expanding scope beyond deterministic insights and recommendations.

## Planning Validation

1. Confirm the feature branch:

   ```powershell
   git branch --show-current
   ```

   Expected: `006-insights-recommendations`.

2. Review the specification and plan:

   ```powershell
   Get-Content specs\006-insights-recommendations\spec.md
   Get-Content specs\006-insights-recommendations\plan.md
   ```

   Expected: Phase 5 is limited to day/week insights, deterministic generation, evidence-backed recommendations, result review, traceability, and history.

3. Review the generated design artifacts:

   ```powershell
   Get-Content specs\006-insights-recommendations\research.md
   Get-Content specs\006-insights-recommendations\data-model.md
   Get-Content specs\006-insights-recommendations\contracts\insights-recommendations-api.yaml
   ```

   Expected: No unresolved clarification markers.

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
   pytest tests/domain tests/services tests/repositories tests/api tests/migrations -q
   ```

3. Run the full backend suite:

   ```powershell
   Set-Location backend
   pytest -q
   ```

## API Behavior Checks

Use seeded data containing saved tracking facts and a completed Phase 4 `AIInsightRun`.

1. Generate or reuse a weekly insight result:

   ```http
   POST /api/v1/ai-insights/results/generate
   Authorization: Bearer <token>
   Content-Type: application/json

   {
     "period_granularity": "weekly",
     "anchor_date": "2026-04-15"
   }
   ```

   Expected: success envelope with a completed result or a handled missing-analysis/no-data response. Repeating the same request for the same source analysis returns `reused_existing: true`.

2. Explicitly rerun an existing result:

   ```http
   POST /api/v1/ai-insights/results/{insight_result_id}/rerun
   Authorization: Bearer <token>
   ```

   Expected: a new historical result is created when validation passes and becomes current.

3. Fetch the current result:

   ```http
   GET /api/v1/ai-insights/results/current?period_granularity=weekly&anchor_date=2026-04-15
   Authorization: Bearer <token>
   ```

   Expected: current result includes productivity score or insufficient-data reason, weekly consistency score or insufficient-data reason, best/worst day findings when valid, recommendations, evidence, source analysis reference, generated timestamp, and validation outcome.

4. Verify privacy:

   Expected: response payloads include task names, durations, categories, and tags when used as evidence, but no task note text.

5. Fetch history:

   ```http
   GET /api/v1/ai-insights/results?page=1&limit=20&period_granularity=weekly
   Authorization: Bearer <token>
   ```

   Expected: page/limit pagination metadata and result items in newest-first order.

## Frontend Smoke Checks

Run after frontend tasks are complete.

1. Execute frontend tests:

   ```powershell
   Set-Location frontend
   npm run test
   ```

2. Build the frontend:

   ```powershell
   Set-Location frontend
   npm run build
   ```

3. Manually review `/dashboard/ai-insights`:

   Expected:

   - The user can select a supported day or week.
   - Generate uses the backend API and shows reused/current behavior clearly.
   - Scores show numeric values only when valid and otherwise show insufficient-data reasons.
   - Weekly best/worst day findings are omitted or explained when fewer than three tracked days exist.
   - Recommendations are capped at three and show action, rationale, expected benefit, confidence, priority, and evidence.
   - Older results show source period and source analysis reference.

## Out-of-Scope Guardrails

The implementation must not add:

- New AI provider calls for Phase 5 generation.
- Month or custom date range insights.
- Scheduled generation or automation.
- CSV import behavior.
- Dashboard redesign.
- Report export.
- Notion synchronization.
- AI chat.
