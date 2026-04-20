"use client";

import React from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import type { DashboardOverviewData } from "@/features/analytics/types";

type PeriodTimeTimelineProps = {
  points: DashboardOverviewData["period_timeline"];
};

export function PeriodTimeTimeline({ points }: PeriodTimeTimelineProps) {
  return (
    <section aria-label="Productivity trend over time" className="rounded-3xl border border-line bg-white p-5 shadow-card">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold tracking-tight text-ink">Productivity trend over time</h2>
          <p className="mt-1 text-sm text-muted">Tracked focus minutes by date with hoverable trend context.</p>
        </div>
        <span className="rounded-full border border-indigo-100 bg-indigo-50 px-3 py-1 text-xs font-semibold text-primary">
          {points.length} days
        </span>
      </div>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={points} margin={{ top: 8, right: 12, left: 0, bottom: 8 }}>
            <CartesianGrid stroke="#E2E8F0" strokeDasharray="4 4" vertical={false} />
            <XAxis dataKey="date" tick={{ fontSize: 12, fill: "#64748B" }} tickMargin={8} />
            <YAxis tick={{ fontSize: 12, fill: "#64748B" }} width={44} />
            <Tooltip formatter={(value) => [`${value}m`, "Tracked"]} />
            <Bar dataKey="total_minutes" fill="#4F46E5" radius={[8, 8, 2, 2]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
