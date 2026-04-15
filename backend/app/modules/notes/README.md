# Notes Module

Owns future task-level notes, note history, search, and filtering.

Phase 1 owns the `Note` ORM model, repository, and service rules for treating
empty note input as absent and enforcing one active note per task. Day-level
notes and search remain outside this phase.
