"use client";

import React from "react";
import { useDayDetail } from "../hooks";

type TasksTableProps = {
  selectedDate?: string;
};

const priorities = ["High", "Medium", "Low"] as const;
const statuses = ["Completed", "In progress", "Queued"] as const;

function statusClass(status: (typeof statuses)[number]) {
  if (status === "Completed") return "border-emerald-200 bg-emerald-50 text-success";
  if (status === "In progress") return "border-amber-200 bg-amber-50 text-warning";
  return "border-slate-200 bg-slate-50 text-muted";
}

function priorityClass(priority: (typeof priorities)[number]) {
  if (priority === "High") return "text-danger";
  if (priority === "Medium") return "text-warning";
  return "text-success";
}

export function TasksTable({ selectedDate }: TasksTableProps) {
  const detailQuery = useDayDetail(selectedDate);
  const tasks = detailQuery.data?.tasks ?? [];

  return (
    <section className="overflow-hidden rounded-3xl border border-line bg-white shadow-card">
      <div className="flex flex-col gap-2 border-b border-line p-5 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold tracking-tight text-ink">Tasks table</h2>
          <p className="mt-1 text-sm text-muted">Task name, category, priority, status, duration, and completion date.</p>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-muted">
          {selectedDate ?? "No day selected"}
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[760px] border-collapse text-left text-sm">
          <thead>
            <tr className="border-b border-line bg-slate-50 text-xs font-semibold uppercase tracking-[0.16em] text-muted">
              <th className="px-5 py-3">Task name</th>
              <th className="px-5 py-3">Category</th>
              <th className="px-5 py-3">Priority</th>
              <th className="px-5 py-3">Status</th>
              <th className="px-5 py-3">Duration</th>
              <th className="px-5 py-3">Completion date</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {detailQuery.isLoading ? (
              <tr>
                <td className="px-5 py-5 text-muted" colSpan={6}>
                  Loading tasks...
                </td>
              </tr>
            ) : null}
            {!detailQuery.isLoading && tasks.length === 0 ? (
              <tr>
                <td className="px-5 py-5 text-muted" colSpan={6}>
                  Select a populated daily log to inspect task rows.
                </td>
              </tr>
            ) : null}
            {tasks.map((task, index) => {
              const priority = priorities[index % priorities.length];
              const status = statuses[index % statuses.length];
              return (
                <tr className="transition hover:bg-slate-50" key={task.id}>
                  <td className="px-5 py-4">
                    <details>
                      <summary className="cursor-pointer font-semibold text-ink transition hover:text-primary">
                        {task.title}
                      </summary>
                      <p className="mt-2 max-w-xl text-sm leading-6 text-muted">
                        Source: {task.source}. AI recommendation: preserve this work type inside a focused category
                        block and review duration variance during planning.
                      </p>
                    </details>
                  </td>
                  <td className="px-5 py-4 text-muted">{task.category}</td>
                  <td className={`px-5 py-4 font-semibold ${priorityClass(priority)}`}>{priority}</td>
                  <td className="px-5 py-4">
                    <span className={`rounded-full border px-2 py-1 text-xs font-semibold ${statusClass(status)}`}>
                      {status}
                    </span>
                  </td>
                  <td className="px-5 py-4 font-mono font-semibold text-primary">{task.display_time}</td>
                  <td className="px-5 py-4 text-muted">{selectedDate}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
