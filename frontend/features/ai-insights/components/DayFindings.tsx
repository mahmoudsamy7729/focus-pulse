import React from "react";
import type { DayFinding } from "../schemas";

type DayFindingsProps = {
  bestDayFinding?: DayFinding | null;
  worstDayFinding?: DayFinding | null;
};

export function DayFindings({ bestDayFinding, worstDayFinding }: DayFindingsProps) {
  const findings = [bestDayFinding, worstDayFinding].filter(Boolean) as DayFinding[];
  if (!findings.length) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-base font-semibold text-ink">Day findings</h2>
        <p className="mt-2 text-sm leading-6 text-muted">Weekly day comparisons appear when at least three tracked days create a clear enough signal.</p>
      </section>
    );
  }
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-base font-semibold text-ink">Day findings</h2>
      <div className="mt-3 grid gap-3 md:grid-cols-2">
        {findings.map((finding) => (
          <article className="rounded-lg bg-slate-50 p-3" key={`${finding.finding_type}-${finding.date ?? "none"}`}>
            <p className="text-sm font-semibold text-ink">{finding.label}</p>
            <p className="mt-1 text-sm leading-6 text-muted">{finding.summary}</p>
            {finding.tie_or_close_ranking ? <p className="mt-2 text-xs font-semibold text-slate-600">Tie or close ranking</p> : null}
          </article>
        ))}
      </div>
    </section>
  );
}
