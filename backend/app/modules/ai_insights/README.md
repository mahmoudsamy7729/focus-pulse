# AI Insights Module

Owns AI insight orchestration, input preparation, generated insight storage,
and AI run history.

AI may read validated productivity data and write separate insight outputs. AI
must never mutate source logs, tasks, notes, or imports.

Future AI work must keep run status, input period, model, output, and failure
context traceable.

Phase 1 owns `AIInsightRun` and `AIInsightRunSource` traceability records plus
the service rules for daily/weekly target-period validation, source links,
status transitions, and rerun history. Prompt execution and generated insight
content remain outside this phase.

Phase 4 adds requestable daily and weekly combined analysis runs. AI input
preparation reads task names, durations, categories, tags, and aggregate totals
only. Note text is excluded from provider input, retained source summaries, and
stored outputs. Full structured provider inputs are not persisted after source
references, aggregate summaries, instruction metadata, output, and failure
metadata are recorded.

Combined outputs must contain a summary, detected patterns, behavior insights,
supporting evidence, limitations, generated timestamp, and output outcome. Every
observation must cite supporting evidence from the selected period. Unsupported
claims are rejected by output validation or represented as limitations. Celery
workers stay thin and delegate analysis behavior to module services.
