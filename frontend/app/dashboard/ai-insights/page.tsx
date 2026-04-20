"use client";

import { useMemo, useState } from "react";
import { DayFindings } from "@/features/ai-insights/components/DayFindings";
import { EvidenceList } from "@/features/ai-insights/components/EvidenceList";
import { InsightHistoryList } from "@/features/ai-insights/components/InsightHistoryList";
import { InsightPeriodPicker } from "@/features/ai-insights/components/InsightPeriodPicker";
import { RecommendationList } from "@/features/ai-insights/components/RecommendationList";
import { ScoreExplanation } from "@/features/ai-insights/components/ScoreExplanation";
import { useCurrentInsightResult } from "@/features/ai-insights/hooks/use-current-insight-result";
import { useGenerateInsightResult } from "@/features/ai-insights/hooks/use-generate-insight-result";
import { useInsightResultHistory } from "@/features/ai-insights/hooks/use-insight-result-history";
import { useRerunInsightResult } from "@/features/ai-insights/hooks/use-rerun-insight-result";
import type { PeriodGranularity } from "@/features/ai-insights/schemas";

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

export default function AIInsightsPage() {
  const [periodGranularity, setPeriodGranularity] = useState<PeriodGranularity>("weekly");
  const [anchorDate, setAnchorDate] = useState(todayIso());
  const currentQuery = useCurrentInsightResult(periodGranularity, anchorDate);
  const historyQuery = useInsightResultHistory(periodGranularity);
  const generateMutation = useGenerateInsightResult(periodGranularity, anchorDate);
  const rerunMutation = useRerunInsightResult();
  const currentResult = currentQuery.data?.current_result ?? generateMutation.data?.result ?? null;
  const statusMessage = useMemo(() => {
    if (generateMutation.data?.reused_existing) {
      return "Existing current result reused for this source analysis.";
    }
    if (generateMutation.data) {
      return "New result generated and marked current.";
    }
    if (currentResult) {
      return "Current result is ready.";
    }
    return "Choose a day or week with completed source analysis.";
  }, [currentResult, generateMutation.data]);

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-6 text-ink md:px-8">
      <div className="mx-auto grid max-w-6xl gap-6">
        <section className="grid gap-5 border-b border-slate-200 pb-6">
          <div>
            <p className="text-sm font-semibold uppercase text-cyan-700">AI insights</p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight text-ink">Scores, evidence, and recommendations</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-muted">
              Generate deterministic day or week results from completed analysis and saved tracking facts.
            </p>
          </div>
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <InsightPeriodPicker
              periodGranularity={periodGranularity}
              anchorDate={anchorDate}
              onPeriodGranularityChange={setPeriodGranularity}
              onAnchorDateChange={setAnchorDate}
            />
            <button
              className="h-11 rounded-lg bg-ink px-4 text-sm font-semibold text-white disabled:opacity-50"
              type="button"
              disabled={generateMutation.isPending}
              onClick={() => generateMutation.mutate()}
            >
              {generateMutation.isPending ? "Generating" : "Generate"}
            </button>
          </div>
          <p className="text-sm font-medium text-slate-600">{statusMessage}</p>
          {generateMutation.error ? <p className="text-sm font-semibold text-red-700">{generateMutation.error.message}</p> : null}
        </section>

        {currentQuery.isLoading ? <p className="text-sm text-muted">Loading current result.</p> : null}
        {currentResult ? (
          <div className="grid gap-5">
            <section className="grid gap-4 md:grid-cols-2">
              <ScoreExplanation title="Productivity" score={currentResult.productivity_score} />
              <ScoreExplanation title="Consistency" score={currentResult.consistency_score} />
            </section>
            <DayFindings bestDayFinding={currentResult.best_day_finding} worstDayFinding={currentResult.worst_day_finding} />
            <RecommendationList recommendations={currentResult.recommendations} />
            <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
              <h2 className="text-base font-semibold text-ink">Evidence</h2>
              <div className="mt-3">
                <EvidenceList evidence={currentResult.evidence} />
              </div>
            </section>
          </div>
        ) : (
          <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-ink">No current result</h2>
            <p className="mt-2 text-sm leading-6 text-muted">Generate a result after the matching source analysis has completed.</p>
          </section>
        )}

        <InsightHistoryList
          items={historyQuery.data?.items ?? []}
          rerunning={rerunMutation.isPending}
          onRerun={(resultId) => rerunMutation.mutate(resultId)}
        />
      </div>
    </main>
  );
}
