import React from "react";
import type { InsightEvidence } from "../schemas";

type EvidenceListProps = {
  evidence: InsightEvidence[];
};

export function EvidenceList({ evidence }: EvidenceListProps) {
  if (!evidence.length) {
    return <p className="text-sm text-muted">No evidence is attached to this result.</p>;
  }
  return (
    <section className="grid gap-3">
      {evidence.map((item) => (
        <article className="rounded-lg border border-slate-200 bg-white p-3 text-sm shadow-sm" key={item.evidence_id}>
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-lg bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-700">{item.evidence_type}</span>
            {item.source_date ? <span className="text-xs font-medium text-slate-500">{item.source_date}</span> : null}
          </div>
          <p className="mt-2 leading-6 text-ink">{item.summary}</p>
        </article>
      ))}
    </section>
  );
}
