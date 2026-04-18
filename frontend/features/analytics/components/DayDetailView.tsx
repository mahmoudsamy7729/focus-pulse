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
    return <EmptyState title="Select a day" message="Choose a daily log to inspect its tasks." />;
  }

  if (detailQuery.isLoading) {
    return <div className="rounded-lg border border-line bg-white p-4 text-sm text-gray-600">Loading day detail...</div>;
  }

  if (detailQuery.isError || !detailQuery.data) {
    return <EmptyState title="Day detail unavailable" message="The selected day could not be loaded." />;
  }

  const detail = detailQuery.data;
  if (detail.empty_state) {
    return <EmptyState message={detail.empty_state.message} />;
  }

  return (
    <section aria-label="Day detail" className="rounded-lg border border-line bg-white p-4">
      <div className="flex flex-col gap-2 border-b border-line pb-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-xl font-semibold">{detail.date}</h2>
          <p className="text-sm text-gray-600">
            {detail.task_count} tasks, {detail.display_total}
          </p>
        </div>
      </div>
      <ol className="mt-4 grid gap-3">
        {detail.tasks.map((task) => (
          <li key={task.id} className="grid gap-2 rounded-lg border border-line p-3">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <p className="font-medium text-ink">
                {task.timeline_position + 1}. {task.title}
              </p>
              <span className="text-sm font-semibold text-mint">{task.display_time}</span>
            </div>
            <p className="text-sm text-gray-700">{task.category}</p>
            {task.tags.length > 0 ? (
              <div className="flex flex-wrap gap-2" aria-label="Task tags">
                {task.tags.map((tag) => (
                  <span key={tag} className="rounded-md bg-gray-100 px-2 py-1 text-xs text-gray-700">
                    {tag}
                  </span>
                ))}
              </div>
            ) : null}
            {task.note ? <p className="text-sm text-gray-600">{task.note}</p> : null}
          </li>
        ))}
      </ol>
    </section>
  );
}
