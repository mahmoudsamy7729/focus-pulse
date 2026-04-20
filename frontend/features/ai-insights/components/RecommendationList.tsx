import React from "react";
import type { Recommendation } from "../schemas";

type RecommendationListProps = {
  recommendations: Recommendation[];
};

export function RecommendationList({ recommendations }: RecommendationListProps) {
  if (!recommendations.length) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-base font-semibold text-ink">Recommendations</h2>
        <p className="mt-2 text-sm leading-6 text-muted">No recommendation met the evidence threshold for this result.</p>
      </section>
    );
  }
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-base font-semibold text-ink">Recommendations</h2>
      <div className="mt-3 grid gap-3">
        {recommendations.map((recommendation) => (
          <article className="rounded-lg bg-white p-3 ring-1 ring-slate-200" key={recommendation.recommendation_id}>
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded-lg bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-800">
                Priority {recommendation.priority}
              </span>
              <span className="rounded-lg bg-cyan-50 px-2 py-1 text-xs font-semibold text-cyan-800">{recommendation.confidence}</span>
            </div>
            <p className="mt-3 font-semibold text-ink">{recommendation.action}</p>
            <p className="mt-2 text-sm leading-6 text-muted">{recommendation.rationale}</p>
            <p className="mt-2 text-sm leading-6 text-slate-700">{recommendation.expected_benefit}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
