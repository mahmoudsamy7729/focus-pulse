# AI Insights Feature

Owns AI insight views, result review, and AI-insight-specific frontend logic.

Phase 5 provides the `/dashboard/ai-insights` review flow. The feature supports
day and week periods, current result lookup, deterministic result generation,
explicit reruns, history, score explanations, weekly day findings,
recommendations, and evidence rendering.

Server state stays in TanStack Query hooks under `hooks/`. API payload types and
Zod schemas stay in `schemas.ts`, and route files under `frontend/app/` only
compose feature components.
