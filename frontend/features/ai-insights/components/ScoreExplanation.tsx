import React from "react";
import type { ScoreOutcome } from "../schemas";

type ScoreExplanationProps = {
  title: string;
  score: ScoreOutcome | null | undefined;
};

export function ScoreExplanation({ title, score }: ScoreExplanationProps) {
  if (!score) {
    return null;
  }
  const scoreLabel = score.state === "scored" ? `${score.score}/100` : score.state.replace("_", " ");
  return (
    <article className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase text-slate-500">{title}</p>
          <h2 className="mt-1 text-2xl font-semibold text-ink">{scoreLabel}</h2>
        </div>
        <span className="rounded-lg bg-cyan-50 px-2 py-1 text-xs font-semibold text-cyan-700">{score.confidence}</span>
      </div>
      <p className="mt-3 text-sm leading-6 text-muted">{score.summary}</p>
      {score.insufficient_data_reason ? <p className="mt-2 text-sm text-slate-600">{score.insufficient_data_reason}</p> : null}
      <div className="mt-4 grid gap-3 md:grid-cols-2">
        {score.positive_factors.map((factor) => (
          <div className="rounded-lg bg-emerald-50 p-3 text-sm" key={factor.label}>
            <p className="font-semibold text-emerald-800">{factor.label}</p>
            <p className="mt-1 leading-6 text-emerald-900">{factor.explanation}</p>
          </div>
        ))}
        {score.limiting_factors.map((factor) => (
          <div className="rounded-lg bg-amber-50 p-3 text-sm" key={factor.label}>
            <p className="font-semibold text-amber-800">{factor.label}</p>
            <p className="mt-1 leading-6 text-amber-900">{factor.explanation}</p>
          </div>
        ))}
      </div>
    </article>
  );
}
