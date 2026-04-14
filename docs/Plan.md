# Daily Tracker Dashboard — Final Project Plan

## Project Overview
This project builds a personal productivity system that:
- ingests daily logs from Notion CSV exports
- normalizes and stores structured data
- analyzes behavior using AI
- provides a dashboard with actionable insights

The system is built using a **phase-based, spec-driven approach** aligned with a **modular monolith architecture**.

---

## Development Strategy

Each phase is implemented as a **separate Spec Kit spec**.

### Workflow per Phase
1. /speckit.constitution
2. /speckit.specify
3. /speckit.plan
4. /speckit.tasks
5. Implement ONLY that phase

### Branch Strategy
- One branch per phase
- One spec folder per phase
- No multi-phase implementation in one cycle

---

# 🧱 Phase 0 — Foundation & Architecture

## Goal
Define project rules, scope, and architecture.

## Scope
- product purpose
- architecture rules
- naming conventions
- tech stack decisions
- non-functional requirements
- v1 scope boundaries

## Decisions to Lock
- backend: FastAPI
- frontend: Next.js
- database: PostgreSQL
- jobs: Celery + Redis
- AI boundaries
- CSV-first ingestion

## Acceptance Criteria
- Clear architecture rules
- Defined project boundaries
- Consistent conventions

---

# 🧩 Phase 1 — Core Domain & Data Model

## Goal
Design a scalable data model for daily tracking.

## Core Entities
- DailyLog
- Task
- Category
- Tag
- Note
- ImportRun
- AIInsightRun

## Requirements
- Tasks linked to a day
- Tags stored as JSON array
- Categories normalized
- Import traceability

## Acceptance Criteria
- Clean relationships
- Future-proof schema

---

# 📥 Phase 2 — CSV Import Pipeline

## Goal
Convert CSV data into structured DB records.

## CSV Contract
Required:
- date
- task
- category
- time_spent_minutes

Optional:
- tags
- notes

## Normalization Rules
- lowercase all text
- trim spaces
- tags → array
- unique tags
- empty tags → []
- empty notes → null

## Features
- upload CSV
- preview parsed data
- validation
- normalization
- insert data
- track import run

## Deduplication
- based on (date + task + time_spent_minutes)

## Background Jobs
- async processing
- status tracking

## Acceptance Criteria
- valid rows inserted
- invalid rows logged
- import traceable

---

# 📊 Phase 3 — Dashboard Foundation

## Goal
Provide a usable dashboard.

## Features
- daily logs list
- day detail view
- time summaries
- category breakdown
- tag breakdown
- filters (day/week/month)

## UI Components
- summary cards
- timeline view
- charts

## Acceptance Criteria
- easy navigation
- fast filtering
- clear data visualization

---

# 🤖 Phase 4 — AI Analysis Engine

## Goal
Analyze productivity data.

## Features
- daily summary
- weekly summary
- pattern detection
- behavior insights

## Design
- structured input
- prompt templates
- store outputs
- rerun support

## Jobs
- async execution
- retry support

## Acceptance Criteria
- reliable outputs
- stored results
- traceable failures

---

# 💡 Phase 5 — Insights & Recommendations

## Goal
Convert AI output into actionable insights.

## Features
- productivity score
- consistency score
- best/worst days
- recommendations

## Principles
- explainable insights
- no noise

## Acceptance Criteria
- useful recommendations
- clear value to user

---

# ⚙️ Phase 6 — Automation & Reliability

## Goal
Make system production-ready.

## Features
- scheduled imports
- scheduled AI runs
- retries
- logs

## Acceptance Criteria
- stable daily usage
- recoverable failures

---

# 🎨 Phase 7 — UX & Future Integrations

## Goal
Improve UX and scalability.

## Features
- UI polish
- performance improvements
- export reports
- Notion API (future)
- AI chat (future)

---

# 🧩 Mapping Phases to Modules

## Phase 1
- daily_logs
- tasks
- notes
- imports

## Phase 2
- imports
- tasks
- notes
- daily_logs

## Phase 3
- analytics
- daily_logs
- tasks

## Phase 4
- ai_insights
- analytics

## Phase 5
- ai_insights
- analytics

## Phase 6
- workers
- imports
- ai_insights

---

# 🚀 v1 Scope

Build:
- Phase 1
- Phase 2
- Phase 3
- Basic Phase 4

## Result
- working system
- real data
- usable dashboard
- basic AI insights

---

# 🔥 Critical Rules

1. No business logic in routers
2. No DB logic outside repositories
3. Import pipeline must be reliable
4. AI logic isolated in ai_insights module
5. Use async jobs for heavy operations

---

# Final Note

Build this project incrementally.
Do not skip phases.
Data quality is the foundation of everything.

