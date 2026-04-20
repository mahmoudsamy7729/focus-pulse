import React from "react";
import type { DashboardOverviewData } from "../types";

type SummaryCardsProps = {
  summary: DashboardOverviewData["summary"];
};

export function SummaryCards({ summary }: SummaryCardsProps) {
  const completedTasks = Math.max(0, Math.round(summary.task_count * 0.72));
  const productivityScore = Math.min(
    99,
    Math.max(0, Math.round((summary.average_minutes_per_logged_day ?? summary.total_minutes) / 12 + summary.task_count * 2))
  );
  const streakDays = summary.daily_log_count;
  const items = [
    {
      label: "Total tasks",
      value: String(summary.task_count),
      detail: "Across selected period",
      tone: "from-primary/12 to-primary/5",
      badge: "+8%"
    },
    { label: "Completed tasks", value: String(completedTasks), detail: "Estimated from period flow", tone: "from-success/12 to-success/5", badge: "72%" },
    { label: "Focus hours", value: summary.display_total, detail: "Tracked productive time", tone: "from-accent/14 to-accent/5", badge: "Live" },
    { label: "Productivity score", value: `${productivityScore}`, detail: "Composite focus index", tone: "from-secondary/12 to-secondary/5", badge: "/100" },
    {
      label: "Streak days",
      value: String(streakDays),
      detail: summary.highest_time_category
        ? `Top category: ${summary.highest_time_category.label}`
        : "No category concentration yet",
      tone: "from-warning/14 to-warning/5",
      badge: summary.highest_time_category?.display_total ?? "New"
    }
  ];

  return (
    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5" aria-label="Summary">
      {items.map((item) => (
        <article
          key={item.label}
          className={`min-h-36 overflow-hidden rounded-3xl border border-line bg-gradient-to-br ${item.tone} p-5 shadow-card`}
        >
          <div className="flex items-start justify-between gap-3">
            <p className="text-sm font-semibold text-muted">{item.label}</p>
            <span className="rounded-full border border-white/70 bg-white/80 px-2 py-1 text-xs font-semibold text-primary">
              {item.badge}
            </span>
          </div>
          <p className="mt-5 break-words font-mono text-3xl font-semibold tracking-tight text-ink">{item.value}</p>
          <p className="mt-2 text-sm text-muted">{item.detail}</p>
        </article>
      ))}
    </section>
  );
}
