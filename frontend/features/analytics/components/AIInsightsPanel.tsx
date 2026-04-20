import React from "react";
import type { DashboardOverviewData } from "../types";

type AIInsightsPanelProps = {
  summary: DashboardOverviewData["summary"];
};

const insights = [
  {
    label: "Summary",
    tone: "text-primary bg-indigo-50 border-indigo-100",
    title: "Focus quality is trending upward",
    copy: "Longer category blocks suggest fewer interruptions during the selected period."
  },
  {
    label: "Recommendation",
    tone: "text-accent bg-cyan-50 border-cyan-100",
    title: "Protect the first deep-work window",
    copy: "Reserve the highest-energy morning block for strategic tasks before admin work begins."
  },
  {
    label: "Risk alert",
    tone: "text-danger bg-red-50 border-red-100",
    title: "Task fragmentation risk",
    copy: "If average task duration keeps dropping, batch small work into one operating block."
  },
  {
    label: "Highlight",
    tone: "text-success bg-emerald-50 border-emerald-100",
    title: "Strong category concentration",
    copy: "The top category is creating a clear signal for planning and retrospective reviews."
  }
];

export function AIInsightsPanel({ summary }: AIInsightsPanelProps) {
  return (
    <section className="rounded-3xl border border-indigo-100 bg-gradient-to-br from-white via-indigo-50/60 to-cyan-50/70 p-5 shadow-card">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-primary">AI insights</p>
          <h2 className="mt-1 text-lg font-semibold tracking-tight text-ink">Generated productivity intelligence</h2>
          <p className="mt-1 text-sm leading-6 text-muted">
            Draft recommendations based on {summary.display_total} of tracked work.
          </p>
        </div>
        <span className="rounded-full bg-white px-3 py-1 text-xs font-semibold text-success shadow-sm">Ready</span>
      </div>
      <div className="mt-5 grid gap-3">
        {insights.map((insight) => (
          <article className="rounded-2xl border border-white/70 bg-white/82 p-4 shadow-sm" key={insight.label}>
            <span className={`inline-flex rounded-full border px-2 py-1 text-xs font-semibold ${insight.tone}`}>
              {insight.label}
            </span>
            <h3 className="mt-3 text-sm font-semibold text-ink">{insight.title}</h3>
            <p className="mt-1 text-sm leading-6 text-muted">{insight.copy}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
