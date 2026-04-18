import React from "react";
import type { DashboardOverviewData } from "../types";

type SummaryCardsProps = {
  summary: DashboardOverviewData["summary"];
};

export function SummaryCards({ summary }: SummaryCardsProps) {
  const items = [
    { label: "Tracked time", value: summary.display_total },
    { label: "Tasks", value: String(summary.task_count) },
    { label: "Logged days", value: String(summary.daily_log_count) },
    {
      label: "Top category",
      value: summary.highest_time_category
        ? `${summary.highest_time_category.label} (${summary.highest_time_category.display_total})`
        : "None"
    },
    {
      label: "Average logged day",
      value:
        summary.average_minutes_per_logged_day === null
          ? "Not applicable"
          : `${summary.average_minutes_per_logged_day}m`
    }
  ];

  return (
    <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5" aria-label="Summary">
      {items.map((item) => (
        <article key={item.label} className="min-h-28 rounded-lg border border-line bg-white p-4">
          <p className="text-sm text-gray-600">{item.label}</p>
          <p className="mt-3 break-words text-2xl font-semibold text-ink">{item.value}</p>
        </article>
      ))}
    </section>
  );
}
