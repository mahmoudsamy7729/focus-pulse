import "@testing-library/jest-dom/vitest";
import React from "react";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { EvidenceList } from "./EvidenceList";
import { InsightPeriodPicker } from "./InsightPeriodPicker";
import { ScoreExplanation } from "./ScoreExplanation";

describe("Insight score review components", () => {
  afterEach(() => cleanup());

  it("renders supported period selection, score explanations, insufficient data, and evidence without note text", () => {
    render(
      <>
        <InsightPeriodPicker
          periodGranularity="weekly"
          anchorDate="2026-04-15"
          onPeriodGranularityChange={() => undefined}
          onAnchorDateChange={() => undefined}
        />
        <ScoreExplanation
          title="Productivity"
          score={{
            score_type: "productivity",
            state: "scored",
            score: 72,
            confidence: "medium",
            summary: "Productivity score is evidence-backed.",
            positive_factors: [],
            limiting_factors: [],
            evidence_ids: ["task-count", "category-1"],
            insufficient_data_reason: null
          }}
        />
        <ScoreExplanation
          title="Consistency"
          score={{
            score_type: "consistency",
            state: "insufficient_data",
            score: null,
            confidence: "low",
            summary: "At least three tracked days are needed.",
            positive_factors: [],
            limiting_factors: [],
            evidence_ids: [],
            insufficient_data_reason: "Weekly consistency requires at least three tracked days."
          }}
        />
        <EvidenceList
          evidence={[
            {
              evidence_id: "task-count",
              evidence_type: "task_count",
              count: 2,
              summary: "2 tracked tasks."
            }
          ]}
        />
      </>
    );

    expect(screen.getByLabelText("Period")).toHaveValue("weekly");
    expect(screen.getByText("72/100")).toBeInTheDocument();
    expect(screen.getByText("insufficient data")).toBeInTheDocument();
    expect(screen.getByText("2 tracked tasks.")).toBeInTheDocument();
    expect(screen.queryByText(/note text/i)).not.toBeInTheDocument();
  });
});
