# Research: CSV Import Pipeline

## Decision: Preview is side-effect free

**Rationale**: The clarified spec states that preview requests must not create tracking records or ImportRun records. Keeping preview side-effect free lets users inspect validation results repeatedly without polluting import history.

**Alternatives considered**:

- Create an ImportRun for every preview: rejected because it contradicts the clarification and would make history noisy.
- Create a separate PreviewRun model: rejected because Phase 2 does not require persisted preview history.

## Decision: Confirmed import parses the CSV again and enqueues normalized row payloads

**Rationale**: Raw CSV files must not be retained, but confirmed import processing must be asynchronous. Re-parsing the submitted CSV at confirmation time lets the server validate data again, create the ImportRun only after confirmation, and pass normalized row payloads to the worker without storing full raw file contents.

**Alternatives considered**:

- Persist raw CSV between preview and confirm: rejected because the spec chooses metadata and row outcomes only.
- Trust client-submitted preview rows: rejected because the server must remain authoritative for validation and normalization.
- Store transient preview records: rejected because preview persistence is not needed for Phase 2 value.

## Decision: Use standard library CSV parsing

**Rationale**: The CSV contract is small and explicit: required columns are `date`, `task`, `category`, `time_spent_minutes`; optional columns are `tags` and `notes`. Python's standard `csv` module handles quoted delimiters and common CSV escaping without adding a dependency.

**Alternatives considered**:

- Add pandas: rejected as too heavy for request/worker validation and unnecessary for personal-tracker imports.
- Hand-roll string splitting: rejected because quoted CSV values and commas inside fields require a real parser.

## Decision: Accept ISO dates and explicit Notion-style date text

**Rationale**: The spec clarification accepts ISO dates and common Notion date text such as `April 15, 2026`. Implementation can support ISO parsing plus explicit `strptime` formats for full month and abbreviated month names while rejecting ambiguous numeric locale formats.

**Alternatives considered**:

- Accept all locale numeric dates: rejected because `04/05/2026` is ambiguous across locales.
- Require ISO only: rejected because common Notion exports may be human-readable month-name dates.

## Decision: Split tags on commas

**Rationale**: The clarified spec chooses comma-separated tags. The parser should split the optional tags cell on commas, trim values, lowercase values, remove blanks, and de-duplicate while preserving first occurrence order.

**Alternatives considered**:

- Accept commas and semicolons: rejected because broader delimiter rules make user mistakes harder to detect.
- Treat the whole cell as one tag: rejected because it prevents tag breakdowns in later dashboard phases.

## Decision: Use Celery + Redis for confirmed import work

**Rationale**: The constitution and project plan require async processing for heavy operations. Confirmed import submission should return quickly with an ImportRun ID, and a thin Celery task should delegate processing to the import service.

**Alternatives considered**:

- Process confirmed imports synchronously in the request: rejected because Phase 2 requires background processing and status tracking.
- Add a different queue library: rejected because Celery + Redis is already the approved stack.

## Decision: Reuse Phase 1 domain services for persistence

**Rationale**: Phase 1 already defines DailyLog reuse, Category reuse, Task deduplication, tag normalization, note creation, ImportRun status transitions, and row-outcome traceability. The import pipeline should orchestrate those services instead of duplicating business rules.

**Alternatives considered**:

- Insert rows directly from the import service: rejected because it bypasses service boundaries and duplicates rules.
- Add separate staging tables for all rows: rejected because Phase 2 does not require raw or full-row persistence for inserted rows.

## Decision: API endpoints are protected, versioned, and rate-limited by contract

**Rationale**: Upload and import operations are expensive and user-owned. Contracts define `/api/v1/imports` endpoints, `imports:write` and `imports:read` scopes, standard response envelopes, stable error codes, and rate-limit expectations.

**Alternatives considered**:

- Leave endpoints unprotected until auth exists: rejected because the constitution requires protected operations to define scopes and permissions.
- Accept `owner_id` in request payloads: rejected because owner identity should come from authenticated context; tests may override a current-owner dependency.
