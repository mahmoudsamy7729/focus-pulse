"use client";

import React from "react";
import type { InsightResult } from "../schemas";

type InsightHistoryListProps = {
  items: InsightResult[];
  onRerun: (resultId: string) => void;
  rerunning?: boolean;
};

export function InsightHistoryList({ items, onRerun, rerunning }: InsightHistoryListProps) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-base font-semibold text-ink">History</h2>
      <div className="mt-3 grid gap-3">
        {items.length ? (
          items.map((item) => (
            <article className="rounded-lg bg-slate-50 p-3" key={item.id}>
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold text-ink">
                    {item.period_start} to {item.period_end}
                  </p>
                  <p className="mt-1 text-xs text-slate-500">Source analysis {item.source_ai_insight_run_id}</p>
                </div>
                <div className="flex items-center gap-2">
                  {item.is_current ? <span className="rounded-lg bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-800">Current</span> : null}
                  <button
                    className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-semibold text-ink disabled:opacity-50"
                    type="button"
                    disabled={rerunning}
                    onClick={() => onRerun(item.id)}
                  >
                    Rerun
                  </button>
                </div>
              </div>
            </article>
          ))
        ) : (
          <p className="text-sm leading-6 text-muted">Generated results will appear here.</p>
        )}
      </div>
    </section>
  );
}
