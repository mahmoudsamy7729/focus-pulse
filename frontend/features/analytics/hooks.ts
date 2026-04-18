import { useQuery } from "@tanstack/react-query";
import { fetchDashboardOverview, fetchDayDetail } from "./api";
import type { PeriodType } from "./types";

export const analyticsQueryKeys = {
  dashboard: (periodType: PeriodType, anchorDate?: string) => ["analytics", "dashboard", periodType, anchorDate],
  dayDetail: (logDate?: string) => ["daily-logs", logDate]
};

export function useDashboardOverview(periodType: PeriodType, anchorDate?: string) {
  return useQuery({
    queryKey: analyticsQueryKeys.dashboard(periodType, anchorDate),
    queryFn: () => fetchDashboardOverview(periodType, anchorDate)
  });
}

export function useDayDetail(logDate?: string) {
  return useQuery({
    queryKey: analyticsQueryKeys.dayDetail(logDate),
    queryFn: () => fetchDayDetail(logDate as string),
    enabled: Boolean(logDate)
  });
}
