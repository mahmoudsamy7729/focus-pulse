import React from "react";
import type { DashboardOverviewData } from "../types";

type DailyLogsListProps = {
  logs: DashboardOverviewData["daily_logs"];
  selectedDate?: string;
  onSelectDate: (date: string) => void;
};

export function DailyLogsList({ logs, selectedDate, onSelectDate }: DailyLogsListProps) {
  if (logs.length === 0) {
    return <p className="text-sm text-gray-600">No daily logs in this period.</p>;
  }

  return (
    <section aria-label="Daily logs" className="overflow-hidden rounded-lg border border-line bg-white">
      <div className="grid grid-cols-[1fr_auto_auto] gap-3 border-b border-line px-4 py-3 text-sm font-medium text-gray-600">
        <span>Date</span>
        <span>Tasks</span>
        <span>Total</span>
      </div>
      <div className="divide-y divide-line">
        {logs.map((log) => (
          <button
            className={`focus-ring grid w-full grid-cols-[1fr_auto_auto] gap-3 px-4 py-3 text-left text-sm transition ${
              selectedDate === log.date ? "bg-teal-50" : "bg-white hover:bg-gray-50"
            }`}
            key={log.date}
            type="button"
            onClick={() => onSelectDate(log.date)}
            aria-pressed={selectedDate === log.date}
          >
            <span className="font-medium text-ink">{log.date}</span>
            <span className="text-gray-700">{log.task_count}</span>
            <span className="font-medium text-mint">{log.display_total}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
