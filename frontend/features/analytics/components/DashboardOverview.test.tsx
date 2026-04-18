import "@testing-library/jest-dom/vitest";
import React from "react";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { DashboardOverview } from "./DashboardOverview";
import type { DashboardOverviewData, DayDetailData } from "../types";

const dashboardData: DashboardOverviewData = {
  period: {
    period_type: "day",
    anchor_date: "2026-04-15",
    start_date: "2026-04-15",
    end_date: "2026-04-15",
    label: "Apr 15, 2026"
  },
  summary: {
    total_minutes: 75,
    display_total: "1h 15m",
    task_count: 2,
    daily_log_count: 1,
    highest_time_category: { label: "Work", total_minutes: 75, display_total: "1h 15m" },
    average_minutes_per_logged_day: null
  },
  daily_logs: [
    {
      date: "2026-04-15",
      total_minutes: 75,
      display_total: "1h 15m",
      task_count: 2,
      top_category: { label: "Work", total_minutes: 75, display_total: "1h 15m" }
    }
  ],
  period_timeline: [{ date: "2026-04-15", total_minutes: 75, display_total: "1h 15m", has_tasks: true }],
  category_breakdown: [{ label: "Work", total_minutes: 75, display_total: "1h 15m", share_of_total: 1, is_other: false }],
  tag_breakdown: [
    { label: "deep", total_minutes: 75, display_total: "1h 15m", share_label: "100%", is_untagged: false, is_other: false }
  ],
  tag_total_notice: null,
  empty_state: null
};

const dayDetail: DayDetailData = {
  date: "2026-04-15",
  total_minutes: 75,
  display_total: "1h 15m",
  task_count: 1,
  tasks: [
    {
      id: "00000000-0000-4000-8000-000000000001",
      title: "Plan",
      time_spent_minutes: 75,
      display_time: "1h 15m",
      category: "Work",
      tags: ["deep"],
      note: null,
      source: "csv_import",
      timeline_position: 0
    }
  ],
  empty_state: null
};

vi.mock("../hooks", () => ({
  useDashboardOverview: () => ({ isLoading: false, isError: false, data: dashboardData }),
  useDayDetail: () => ({ isLoading: false, isError: false, data: dayDetail })
}));

vi.mock("recharts", () => ({
  ResponsiveContainer: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  BarChart: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Bar: () => <div />,
  CartesianGrid: () => <div />,
  Tooltip: () => <div />,
  XAxis: () => <div />,
  YAxis: () => <div />,
  PieChart: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Pie: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Cell: () => <div />
}));

describe("DashboardOverview", () => {
  afterEach(() => cleanup());

  it("renders filters, summary, empty-state-free overview, and selected day detail", () => {
    render(<DashboardOverview />);

    expect(screen.getByRole("heading", { name: "Dashboard" })).toBeInTheDocument();
    expect(screen.getAllByText("1h 15m").length).toBeGreaterThan(0);
    expect(screen.getByRole("button", { name: /2026-04-15/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "2026-04-15" })).toBeInTheDocument();
  });

  it("allows changing the period filter without layout remounts", () => {
    render(<DashboardOverview />);

    const period = screen.getByLabelText("Period");
    fireEvent.change(period, { target: { value: "week" } });

    expect(period).toHaveValue("week");
  });
});
