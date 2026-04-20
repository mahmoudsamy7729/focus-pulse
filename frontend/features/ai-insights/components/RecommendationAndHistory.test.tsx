import "@testing-library/jest-dom/vitest";
import React from "react";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { InsightHistoryList } from "./InsightHistoryList";
import { RecommendationList } from "./RecommendationList";
import type { InsightResult } from "../schemas";

const result: InsightResult = {
  id: "00000000-0000-4000-8000-000000000111",
  status: "completed",
  is_current: true,
  generation_reason: "default_generate",
  period_granularity: "weekly",
  period_start: "2026-04-13",
  period_end: "2026-04-19",
  source_ai_insight_run_id: "00000000-0000-4000-8000-000000000222",
  source_snapshot: {
    period_granularity: "weekly",
    period_start: "2026-04-13",
    period_end: "2026-04-19",
    source_ai_insight_run_id: "00000000-0000-4000-8000-000000000222",
    source_daily_log_ids: [],
    source_task_ids: [],
    daily_log_count: 3,
    tracked_day_count: 3,
    task_count: 4,
    total_minutes: 300,
    category_totals: [],
    tag_totals: [],
    daily_totals: [],
    phase4_observation_ids: [],
    included_fields: [],
    excluded_fields: ["note_text"]
  },
  productivity_score: {
    score_type: "productivity",
    state: "scored",
    score: 70,
    confidence: "medium",
    summary: "Scored",
    positive_factors: [],
    limiting_factors: [],
    evidence_ids: ["task-count"],
    insufficient_data_reason: null
  },
  consistency_score: null,
  best_day_finding: null,
  worst_day_finding: null,
  recommendations: [],
  evidence: [],
  validation_outcome: {
    passed: true,
    checked_at: "2026-04-19T00:00:00Z",
    validator_version: "test",
    checks: [],
    failure_codes: []
  },
  failure_code: null,
  failure_details: null,
  generated_at: "2026-04-19T00:00:00Z",
  created_at: "2026-04-19T00:00:00Z"
};

describe("Recommendation and history components", () => {
  afterEach(() => cleanup());

  it("renders recommendation action, rationale, confidence, and no-recommendation state", () => {
    const recommendation = {
      recommendation_id: "rec-1",
      priority: 1,
      action: "Protect a focused block for Build before adding smaller tasks.",
      rationale: "Build was the strongest category signal.",
      expected_benefit: "This may preserve the strongest tracked pattern.",
      confidence: "medium" as const,
      evidence_ids: ["category-1"],
      source_links: ["source_snapshot.category_totals"],
      dedupe_key: "protect-build"
    };

    render(
      <>
        <RecommendationList recommendations={[recommendation]} />
        <RecommendationList recommendations={[]} />
      </>
    );

    expect(screen.getByText(recommendation.action)).toBeInTheDocument();
    expect(screen.getByText("medium")).toBeInTheDocument();
    expect(screen.getByText(/No recommendation met the evidence threshold/i)).toBeInTheDocument();
  });

  it("renders history source period, source analysis reference, current marker, and rerun action", () => {
    const onRerun = vi.fn();

    render(<InsightHistoryList items={[result]} onRerun={onRerun} />);
    fireEvent.click(screen.getByRole("button", { name: "Rerun" }));

    expect(screen.getByText("2026-04-13 to 2026-04-19")).toBeInTheDocument();
    expect(screen.getByText(/Source analysis 00000000-0000-4000-8000-000000000222/)).toBeInTheDocument();
    expect(screen.getByText("Current")).toBeInTheDocument();
    expect(onRerun).toHaveBeenCalledWith(result.id);
  });
});
