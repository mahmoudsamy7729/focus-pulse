import type { PeriodGranularity } from "./schemas";

export const insightResultKeys = {
  all: ["ai-insights", "results"] as const,
  current: (periodGranularity: PeriodGranularity, anchorDate: string) =>
    [...insightResultKeys.all, "current", periodGranularity, anchorDate] as const,
  detail: (resultId: string) => [...insightResultKeys.all, "detail", resultId] as const,
  history: (periodGranularity?: PeriodGranularity) => [...insightResultKeys.all, "history", periodGranularity ?? "all"] as const
};
