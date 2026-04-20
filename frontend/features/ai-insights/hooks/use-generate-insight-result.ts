"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { generateInsightResult } from "../api";
import { insightResultKeys } from "../query-keys";
import type { PeriodGranularity } from "../schemas";

export function useGenerateInsightResult(periodGranularity: PeriodGranularity, anchorDate: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => generateInsightResult(periodGranularity, anchorDate),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: insightResultKeys.all });
    }
  });
}
