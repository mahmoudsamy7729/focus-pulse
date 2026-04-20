import React from "react";
import type { DashboardOverviewData } from "../types";

type DailyLogsListProps = {
  logs: DashboardOverviewData["daily_logs"];
  selectedDate?: string;
  onSelectDate: (date: string) => void;
};

export function DailyLogsList({ logs, selectedDate, onSelectDate }: DailyLogsListProps) {
  if (logs.length === 0) {
    return <p className="rounded-3xl border border-line bg-white p-5 text-sm text-muted shadow-card">No daily logs in this period.</p>;
  }

  return (
    <section aria-label="Recent activity feed" className="overflow-hidden rounded-3xl border border-line bg-white shadow-card">
      <div className="border-b border-line px-5 py-4">
        <h2 className="text-lg font-semibold tracking-tight text-ink">Recent activity feed</h2>
        <p className="mt-1 text-sm text-muted">Latest completed tasks, created tasks, and imported daily entries.</p>
      </div>
      <div className="grid grid-cols-[1fr_auto_auto] gap-3 border-b border-line bg-slate-50 px-5 py-3 text-xs font-semibold uppercase tracking-[0.16em] text-muted">
        <span>Date</span>
        <span>Tasks</span>
        <span>Total</span>
      </div>
      <div className="divide-y divide-line">
        {logs.map((log) => (
          <button
            className={`focus-ring grid w-full grid-cols-[1fr_auto_auto] gap-3 px-5 py-4 text-left text-sm transition ${
              selectedDate === log.date ? "bg-indigo-50/80" : "bg-white hover:bg-slate-50"
            }`}
            key={log.date}
            type="button"
            onClick={() => onSelectDate(log.date)}
            aria-pressed={selectedDate === log.date}
          >
            <span>
              <span className="block font-semibold text-ink">{log.date}</span>
              <span className="mt-1 block text-xs text-muted">
                {log.top_category ? `Top: ${log.top_category.label}` : "Imported entry"}
              </span>
            </span>
            <span className="self-center rounded-full bg-slate-100 px-2 py-1 font-semibold text-muted">{log.task_count}</span>
            <span className="self-center font-mono font-semibold text-primary">{log.display_total}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
