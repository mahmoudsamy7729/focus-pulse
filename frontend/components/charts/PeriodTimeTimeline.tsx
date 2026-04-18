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
    <section aria-label="Period timeline" className="rounded-lg border border-line bg-white p-4">
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">Time by date</h2>
        <span className="text-sm text-gray-600">{points.length} days</span>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={points} margin={{ top: 8, right: 12, left: 0, bottom: 8 }}>
            <CartesianGrid stroke="#e5e7eb" vertical={false} />
            <XAxis dataKey="date" tick={{ fontSize: 12 }} tickMargin={8} />
            <YAxis tick={{ fontSize: 12 }} width={44} />
            <Tooltip formatter={(value) => [`${value}m`, "Tracked"]} />
            <Bar dataKey="total_minutes" fill="#0f766e" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
