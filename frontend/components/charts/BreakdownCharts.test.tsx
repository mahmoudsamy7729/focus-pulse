import "@testing-library/jest-dom/vitest";
import React from "react";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { CategoryBreakdownChart } from "./CategoryBreakdownChart";
import { TagBreakdownChart } from "./TagBreakdownChart";

vi.mock("recharts", () => ({
  ResponsiveContainer: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  PieChart: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Pie: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Cell: () => <div />,
  BarChart: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Bar: () => <div />,
  CartesianGrid: () => <div />,
  Tooltip: () => <div />,
  XAxis: () => <div />,
  YAxis: () => <div />
}));

describe("breakdown charts", () => {
  afterEach(() => cleanup());

  it("renders category labels including Other", () => {
    render(
      <CategoryBreakdownChart
        items={[
          { label: "Very long category label that should shorten", total_minutes: 90, display_total: "1h 30m", share_of_total: 0.75, is_other: false },
          { label: "Other", total_minutes: 30, display_total: "30m", share_of_total: 0.25, is_other: true }
        ]}
      />
    );

    expect(screen.getByTitle("Very long category label that should shorten")).toBeInTheDocument();
    expect(screen.getByText("Other")).toBeInTheDocument();
  });

  it("renders tag notice, untagged, and Other labels", () => {
    render(
      <TagBreakdownChart
        notice="Tag totals may exceed total tracked time."
        items={[
          { label: "untagged", total_minutes: 45, display_total: "45m", share_label: "50%", is_untagged: true, is_other: false },
          { label: "Other", total_minutes: 45, display_total: "45m", share_label: "50%", is_untagged: false, is_other: true }
        ]}
      />
    );

    expect(screen.getByText("Tag totals may exceed total tracked time.")).toBeInTheDocument();
    expect(screen.getByText("untagged")).toBeInTheDocument();
    expect(screen.getAllByText("Other").length).toBeGreaterThan(0);
  });
});
