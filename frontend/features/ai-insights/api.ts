import { getApiData, postApiData } from "@/lib/api/client";
import type {
  CurrentInsightResultResponse,
  InsightResult,
  InsightResultMutationResponse,
  InsightResultPage,
  PeriodGranularity
} from "./schemas";

export async function getCurrentInsightResult(periodGranularity: PeriodGranularity, anchorDate: string) {
  return getApiData<CurrentInsightResultResponse>("/ai-insights/results/current", {
    period_granularity: periodGranularity,
    anchor_date: anchorDate
  });
}

export async function generateInsightResult(periodGranularity: PeriodGranularity, anchorDate: string) {
  return postApiData<InsightResultMutationResponse>("/ai-insights/results/generate", {
    period_granularity: periodGranularity,
    anchor_date: anchorDate
  });
}

export async function getInsightResult(resultId: string) {
  return getApiData<InsightResult>(`/ai-insights/results/${resultId}`);
}

export async function rerunInsightResult(resultId: string) {
  return postApiData<InsightResultMutationResponse>(`/ai-insights/results/${resultId}/rerun`);
}

export async function listInsightResults(periodGranularity?: PeriodGranularity) {
  return getApiData<InsightResultPage>("/ai-insights/results", {
    period_granularity: periodGranularity
  });
}
