import "@testing-library/jest-dom/vitest";
import React from "react";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { DayDetailView } from "./DayDetailView";

vi.mock("../hooks", () => ({
  useDayDetail: () => ({
    isLoading: false,
    isError: false,
    data: {
      date: "2026-04-15",
      total_minutes: 90,
      display_total: "1h 30m",
      task_count: 2,
      tasks: [
        {
          id: "00000000-0000-4000-8000-000000000001",
          title: "Plan",
          time_spent_minutes: 30,
          display_time: "30m",
          category: "Work",
          tags: ["deep"],
          note: "Start here",
          source: "csv_import",
          timeline_position: 0
        },
        {
          id: "00000000-0000-4000-8000-000000000002",
          title: "Build",
          time_spent_minutes: 60,
          display_time: "1h",
          category: "Work",
          tags: [],
          note: null,
          source: "csv_import",
          timeline_position: 1
        }
      ],
      empty_state: null
    }
  })
}));

describe("DayDetailView", () => {
  afterEach(() => cleanup());

  it("renders tasks in timeline order with notes and tags", () => {
    render(<DayDetailView selectedDate="2026-04-15" />);

    expect(screen.getByText("1. Plan")).toBeInTheDocument();
    expect(screen.getByText("2. Build")).toBeInTheDocument();
    expect(screen.getByText("Start here")).toBeInTheDocument();
    expect(screen.getByText("deep")).toBeInTheDocument();
  });
});
