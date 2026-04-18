# Research: Dashboard Foundation

## Decision: Compose Dashboard Aggregates in the Backend

**Rationale**: Total tracked time, category share, tag counting, untagged time, latest tracked day, and top-10-plus-Other grouping must be consistent across all dashboard views. Keeping these rules in the backend prevents each frontend chart or list from reimplementing aggregation differently.

**Alternatives considered**:

- Aggregate everything in the frontend from raw task lists: rejected because it duplicates business rules and increases payload size.
- Store precomputed dashboard tables: rejected because Phase 3 is read-only and the personal v1 scale does not justify persistent derived data.

## Decision: Use `analytics` for Overview and `daily_logs` for Day Detail

**Rationale**: The dashboard overview is an analytics concern because it groups and summarizes records across periods. A single day detail is a daily-log read concern because it exposes one day and its tasks. This keeps module ownership aligned with the constitution and existing Phase 1 model boundaries.

**Alternatives considered**:

- Put all dashboard reads in `analytics`: rejected because day detail would move source-record read ownership away from `daily_logs`.
- Add dashboard-specific routers directly under `app/api`: rejected because feature behavior must stay inside feature modules.

## Decision: Use `period_type` and `anchor_date` for Filters

**Rationale**: A single anchor date can resolve day, Monday-to-Sunday week, and full-month ranges. This avoids three different filter shapes and gives the frontend a simple query key.

**Alternatives considered**:

- Accept explicit `start_date` and `end_date`: rejected for the dashboard foundation because the spec only requires day/week/month filters, not arbitrary custom ranges.
- Use separate endpoints for day, week, and month: rejected because it would duplicate response shapes and frontend fetching logic.

## Decision: No Pagination for Dashboard Daily Log Lists

**Rationale**: The dashboard list is bounded by a selected day, week, or calendar month. A month has at most 31 date rows, so pagination would add complexity without user value. This is explicitly different from unbounded import history lists.

**Alternatives considered**:

- Page/limit pagination: rejected because calendar-bounded dashboard rows are small and users need the full period context.
- Cursor pagination: rejected because dashboard period lists are not append-only infinite-scroll data.

## Decision: Top 10 Plus `Other` Grouping Is Server-Side

**Rationale**: The spec requires category and tag charts to show the top 10 contributors and group the rest as `Other` without dropping tracked time. Doing this server-side makes chart totals testable and keeps frontend chart components simple.

**Alternatives considered**:

- Send all categories and tags and let the frontend group them: rejected because grouping would be duplicated across chart and list components.
- Persist `Other` as a category or tag: rejected because `Other` is a visualization bucket, not source data.

## Decision: Tag Breakdown Counts Multi-Tag Tasks Once Per Tag

**Rationale**: The clarified spec requires full task duration to count for each tag and requires the dashboard to communicate that tag totals may exceed total tracked time. The backend response should include a `multi_tag_notice` flag/message when this condition applies.

**Alternatives considered**:

- Split task duration evenly across tags: rejected because it changes the meaning of imported tag labels.
- Count only the first tag: rejected because it hides valid tag associations.

## Decision: Use Hours-and-Minutes Display with Minute Values in Payloads

**Rationale**: The API should keep exact minute values for calculations, tests, sorting, and future reuse. The frontend can display `display_time` strings supplied by the backend or format minutes consistently through a shared frontend utility.

**Alternatives considered**:

- Decimal hours only: rejected because it introduces rounding confusion.
- Minutes only: rejected because large totals are harder to scan in summary cards and charts.

## Decision: Bootstrap the Frontend Runtime in Phase 3

**Rationale**: The existing `frontend/` directory is a skeleton. Phase 3 is the first phase that requires a usable dashboard, so implementation tasks must create the package manifest, App Router files, API client setup, query provider, styling baseline, and dashboard feature folder.

**Alternatives considered**:

- Keep Phase 3 backend-only: rejected because the spec requires UI components, charts, filters, and easy navigation.
- Create a separate app outside `frontend/`: rejected because the constitution requires the documented monorepo frontend structure.

## Decision: Read Endpoints Require Protected Read Scopes

**Rationale**: Dashboard data is user-owned productivity data. Endpoints should require `analytics:read` and `daily_logs:read` even while the current auth dependency is a Phase 1/2 placeholder.

**Alternatives considered**:

- Leave dashboard endpoints unauthenticated for v1: rejected because it conflicts with the constitution's protected operation rules.
- Reuse import scopes: rejected because dashboard reads are separate permissions from import operations.
