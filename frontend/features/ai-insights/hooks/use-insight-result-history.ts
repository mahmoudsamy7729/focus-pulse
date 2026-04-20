"use client";

import { useQuery } from "@tanstack/react-query";
import { listInsightResults } from "../api";
import { insightResultKeys } from "../query-keys";
import type { PeriodGranularity } from "../schemas";

export function useInsightResultHistory(periodGranularity?: PeriodGranularity) {
  return useQuery({
    queryKey: insightResultKeys.history(periodGranularity),
    queryFn: () => listInsightResults(periodGranularity)
  });
}
