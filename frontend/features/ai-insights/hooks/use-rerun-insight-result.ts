"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { rerunInsightResult } from "../api";
import { insightResultKeys } from "../query-keys";

export function useRerunInsightResult() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (resultId: string) => rerunInsightResult(resultId),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: insightResultKeys.all });
    }
  });
}
