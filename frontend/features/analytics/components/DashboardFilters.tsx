import React from "react";
import type { PeriodType } from "../types";

type DashboardFiltersProps = {
  periodType: PeriodType;
  anchorDate: string;
  onPeriodTypeChange: (periodType: PeriodType) => void;
  onAnchorDateChange: (anchorDate: string) => void;
};

const periodOptions: { value: PeriodType; label: string }[] = [
  { value: "day", label: "Day" },
  { value: "week", label: "Week" },
  { value: "month", label: "Month" }
];

export function DashboardFilters({
  periodType,
  anchorDate,
  onPeriodTypeChange,
  onAnchorDateChange
}: DashboardFiltersProps) {
  return (
    <section className="grid gap-5">
      <div className="flex flex-col gap-4 rounded-3xl border border-line bg-white p-5 shadow-card sm:p-6 xl:flex-row xl:items-center xl:justify-between">
        <div className="min-w-0">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-indigo-100 bg-indigo-50 px-3 py-1 text-xs font-semibold text-primary">
            <span className="h-1.5 w-1.5 rounded-full bg-accent" aria-hidden="true" />
            Productivity command center
          </div>
          <h1 className="text-3xl font-semibold tracking-tight text-ink sm:text-4xl">Dashboard</h1>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-muted">
            Monitor task throughput, focus quality, import activity, and AI-generated recommendations from one
            executive-grade workspace.
          </p>
        </div>
        <div className="rounded-2xl bg-gradient-to-br from-primary via-secondary to-accent p-[1px] shadow-glow">
          <div className="rounded-2xl bg-white/95 px-4 py-3">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">Current range</p>
            <p className="mt-1 text-sm font-semibold text-ink">
              {periodType.toUpperCase()} ending {anchorDate}
            </p>
          </div>
        </div>
      </div>

      <div className="rounded-3xl border border-line bg-white p-4 shadow-card">
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-[11rem_11rem_11rem_11rem_1fr]">
          <label className="grid gap-1 text-sm font-medium text-ink">
            Period
            <select
              className="focus-ring h-11 rounded-xl border border-line bg-slate-50 px-3 text-ink transition hover:border-primary/40"
              value={periodType}
              onChange={(event) => onPeriodTypeChange(event.target.value as PeriodType)}
            >
              {periodOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <label className="grid gap-1 text-sm font-medium text-ink">
            Date range
            <input
              className="focus-ring h-11 rounded-xl border border-line bg-slate-50 px-3 text-ink transition hover:border-primary/40"
              type="date"
              value={anchorDate}
              onChange={(event) => onAnchorDateChange(event.target.value)}
            />
          </label>
          <label className="grid gap-1 text-sm font-medium text-ink">
            Status
            <select className="focus-ring h-11 rounded-xl border border-line bg-slate-50 px-3 text-ink transition hover:border-primary/40" defaultValue="all">
              <option value="all">All statuses</option>
              <option value="completed">Completed</option>
              <option value="in-progress">In progress</option>
              <option value="blocked">At risk</option>
            </select>
          </label>
          <label className="grid gap-1 text-sm font-medium text-ink">
            Category
            <select className="focus-ring h-11 rounded-xl border border-line bg-slate-50 px-3 text-ink transition hover:border-primary/40" defaultValue="all">
              <option value="all">All categories</option>
              <option value="deep-work">Deep work</option>
              <option value="planning">Planning</option>
              <option value="admin">Admin</option>
              <option value="meetings">Meetings</option>
            </select>
          </label>
          <label className="grid gap-1 text-sm font-medium text-ink">
            Quick search
            <input
              className="focus-ring h-11 rounded-xl border border-line bg-slate-50 px-3 text-ink transition placeholder:text-slate-400 hover:border-primary/40"
              placeholder="Search tasks, tags, categories..."
              type="search"
            />
          </label>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {["Deep work", "Admin", "Meetings", "Imported", "AI flagged"].map((filter, index) => (
            <button
              className={`focus-ring rounded-full border px-3 py-1.5 text-xs font-semibold transition ${
                index === 0
                  ? "border-transparent bg-gradient-to-r from-primary to-secondary text-white shadow-glow"
                  : "border-line bg-white text-muted hover:border-primary/40 hover:text-primary"
              }`}
              key={filter}
              type="button"
            >
              {filter}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
