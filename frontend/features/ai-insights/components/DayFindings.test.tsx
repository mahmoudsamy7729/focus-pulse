import "@testing-library/jest-dom/vitest";
import React from "react";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { DayFindings } from "./DayFindings";

describe("DayFindings", () => {
  afterEach(() => cleanup());

  it("renders best and lightest day findings with neutral wording", () => {
    render(
      <DayFindings
        bestDayFinding={{
          finding_type: "best_day",
          date: "2026-04-13",
          label: "Highest tracked day",
          summary: "2026-04-13 had the highest tracked total.",
          confidence: "medium",
          evidence_ids: ["date-2026-04-13"],
          tie_or_close_ranking: false
        }}
        worstDayFinding={{
          finding_type: "worst_day",
          date: "2026-04-15",
          label: "Lightest tracked day",
          summary: "2026-04-15 had the lightest tracked total.",
          confidence: "medium",
          evidence_ids: ["date-2026-04-15"],
          tie_or_close_ranking: false
        }}
      />
    );

    expect(screen.getByText("Highest tracked day")).toBeInTheDocument();
    expect(screen.getByText("Lightest tracked day")).toBeInTheDocument();
    expect(screen.queryByText(/worst performance/i)).not.toBeInTheDocument();
  });

  it("renders omitted state when comparison is not supported", () => {
    render(<DayFindings />);

    expect(screen.getByText(/at least three tracked days/i)).toBeInTheDocument();
  });
});
