# Imports Module

Owns CSV upload, parsing, validation, normalization, confirmed import
execution, and import history.

Future import work must preserve traceability by run, source file, status,
summary, failures, and recovery path.

Phase 1 owns `ImportRun` and `ImportRowOutcome` traceability records plus the
service rules for run status transitions, row counts, and invalid/skipped/failed
row outcomes.

Phase 2 adds the CSV parser, side-effect-free preview service, confirmed import
orchestration, thin worker delegation, and owner-scoped status/history APIs.
Preview requests parse and validate uploaded bytes only; they must not create
`ImportRun`, daily tracking, note, task, category, or row outcome records.

Confirmed imports parse the submitted CSV again on the server, create a pending
`ImportRun`, enqueue normalized row payloads, and process rows through existing
daily log, task, note, and trace services. Full raw CSV contents are not stored
in import history or row snapshots.
