# Daily Logs Module

Owns future daily log records, date grouping, summaries, and links to imported
day data.

Phase 1 owns the `DailyLog` ORM model, daily log repository, and service rules
for reusing one active log per owner and calendar date. This module may expose
providers for routers later, but it does not add public endpoints in Phase 1.
