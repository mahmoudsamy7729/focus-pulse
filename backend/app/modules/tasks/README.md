# Tasks Module

Owns future task storage, status, duration, category relations, and daily task
listing.

Phase 1 owns the `Task` and `Category` ORM models, task/category repositories,
and service rules for title/category normalization, positive durations, JSON tag
normalization, and imported duplicate detection. CSV parsing and dashboard
queries remain outside this phase.
