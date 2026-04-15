# Imports Module

Owns future CSV upload, parsing, validation, normalization, execution, and
import history.

Future import work must preserve traceability by run, source file, status,
summary, failures, and recovery path.

Phase 1 owns `ImportRun` and `ImportRowOutcome` traceability records plus the
service rules for run status transitions, row counts, and invalid/skipped/failed
row outcomes. CSV upload and parsing remain outside this phase.
