import React from "react";
import type { DashboardOverviewData } from "../types";

type WeeklyActivityHeatmapProps = {
  logs: DashboardOverviewData["daily_logs"];
};

const fallbackCells = Array.from({ length: 35 }, (_, index) => ({
  date: `Day ${index + 1}`,
  total_minutes: (index * 37) % 240
}));

function intensityClass(totalMinutes: number) {
  if (totalMinutes >= 210) return "bg-primary";
  if (totalMinutes >= 150) return "bg-secondary";
  if (totalMinutes >= 90) return "bg-accent";
  if (totalMinutes > 0) return "bg-indigo-200";
  return "bg-slate-100";
}

export function WeeklyActivityHeatmap({ logs }: WeeklyActivityHeatmapProps) {
  const source = logs.length > 0 ? logs : fallbackCells;
  const cells = Array.from({ length: 35 }, (_, index) => source[index % source.length]);

  return (
    <section aria-label="Weekly activity heatmap" className="rounded-3xl border border-line bg-white p-5 shadow-card">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold tracking-tight text-ink">Weekly activity heatmap</h2>
          <p className="mt-1 text-sm text-muted">Activity density across recent work sessions.</p>
        </div>
        <div className="flex items-center gap-2 text-xs font-medium text-muted">
          <span>Low</span>
          <span className="h-3 w-3 rounded bg-slate-100" />
          <span className="h-3 w-3 rounded bg-indigo-200" />
          <span className="h-3 w-3 rounded bg-accent" />
          <span className="h-3 w-3 rounded bg-secondary" />
          <span>High</span>
        </div>
      </div>
      <div className="mt-5 grid grid-cols-7 gap-2">
        {cells.map((cell, index) => (
          <div
            aria-label={`${cell.date}: ${cell.total_minutes} minutes`}
            className={`h-9 rounded-xl ${intensityClass(cell.total_minutes)} shadow-sm`}
            key={`${cell.date}-${index}`}
            title={`${cell.date}: ${cell.total_minutes} minutes`}
          />
        ))}
      </div>
    </section>
  );
}
