"use client";

import React from "react";
import { useDayDetail } from "../hooks";
import { EmptyState } from "./EmptyState";

type DayDetailViewProps = {
  selectedDate?: string;
};

export function DayDetailView({ selectedDate }: DayDetailViewProps) {
  const detailQuery = useDayDetail(selectedDate);

  if (!selectedDate) {
    return <EmptyState title="Select a day" message="Choose a daily log to inspect its task details and AI recommendations." />;
  }

  if (detailQuery.isLoading) {
    return <div className="rounded-3xl border border-line bg-white p-5 text-sm text-muted shadow-card">Loading day detail...</div>;
  }

  if (detailQuery.isError || !detailQuery.data) {
    return <EmptyState title="Day detail unavailable" message="The selected day could not be loaded." />;
  }

  const detail = detailQuery.data;
  if (detail.empty_state) {
    return <EmptyState message={detail.empty_state.message} />;
  }

  return (
    <section aria-label="Expandable detail panel" className="rounded-3xl border border-line bg-white p-5 shadow-card">
      <div className="flex flex-col gap-2 border-b border-line pb-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">Detail drawer</p>
          <h2 className="mt-1 text-xl font-semibold tracking-tight text-ink">{detail.date}</h2>
          <p className="text-sm text-muted">
            {detail.task_count} tasks, {detail.display_total}
          </p>
        </div>
        <span className="rounded-full bg-gradient-to-r from-primary/10 to-secondary/10 px-3 py-1 text-xs font-semibold text-primary">
          AI ready
        </span>
      </div>
      <ol className="mt-4 grid gap-3">
        {detail.tasks.map((task) => (
          <li key={task.id} className="grid gap-3 rounded-2xl border border-line bg-slate-50 p-3">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <p className="font-medium text-ink">
                {task.timeline_position + 1}. {task.title}
              </p>
              <span className="font-mono text-sm font-semibold text-primary">{task.display_time}</span>
            </div>
            <p className="text-sm font-medium text-muted">{task.category}</p>
            {task.tags.length > 0 ? (
              <div className="flex flex-wrap gap-2" aria-label="Task tags">
                {task.tags.map((tag) => (
                  <span key={tag} className="rounded-full border border-line bg-white px-2 py-1 text-xs font-medium text-muted">
                    {tag}
                  </span>
                ))}
              </div>
            ) : null}
            {task.note ? <p className="rounded-xl bg-white p-3 text-sm leading-6 text-muted">{task.note}</p> : null}
            <details className="group rounded-xl border border-dashed border-indigo-200 bg-white p-3">
              <summary className="cursor-pointer text-sm font-semibold text-primary transition group-open:text-secondary">
                Analytics breakdown and recommendation
              </summary>
              <p className="mt-2 text-sm leading-6 text-muted">
                This task contributed {task.display_time} to {task.category}. Recommendation: batch adjacent work and
                protect a focused block before switching contexts.
              </p>
            </details>
          </li>
        ))}
      </ol>
    </section>
  );
}
