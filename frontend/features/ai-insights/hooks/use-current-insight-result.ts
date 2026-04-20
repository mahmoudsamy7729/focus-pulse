"use client";

import { useQuery } from "@tanstack/react-query";
import { getCurrentInsightResult } from "../api";
import { insightResultKeys } from "../query-keys";
import type { PeriodGranularity } from "../schemas";

export function useCurrentInsightResult(periodGranularity: PeriodGranularity, anchorDate: string) {
  return useQuery({
    queryKey: insightResultKeys.current(periodGranularity, anchorDate),
    queryFn: () => getCurrentInsightResult(periodGranularity, anchorDate)
  });
}
