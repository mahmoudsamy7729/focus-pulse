# AI Insights Module

Owns future AI insight orchestration, input preparation, insight generation,
recommendation storage, and AI run history.

AI may read validated productivity data and write separate insight outputs. AI
must never mutate source logs, tasks, notes, or imports.

Future AI work must keep run status, input period, model, output, and failure
context traceable.

Phase 1 owns `AIInsightRun` and `AIInsightRunSource` traceability records plus
the service rules for daily/weekly target-period validation, source links,
status transitions, and rerun history. Prompt execution and generated insight
content remain outside this phase.
