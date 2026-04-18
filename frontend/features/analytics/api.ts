import { getApiData } from "@/lib/api/client";
import { dashboardOverviewSchema, dayDetailSchema } from "./schemas";
import type { DashboardOverviewData, DayDetailData, PeriodType } from "./types";

export async function fetchDashboardOverview(
  periodType: PeriodType,
  anchorDate?: string
): Promise<DashboardOverviewData> {
  const data = await getApiData<unknown>("/analytics/dashboard", {
    period_type: periodType,
    anchor_date: anchorDate
  });
  return dashboardOverviewSchema.parse(data);
}

export async function fetchDayDetail(logDate: string): Promise<DayDetailData> {
  const data = await getApiData<unknown>(`/daily-logs/${logDate}`);
  return dayDetailSchema.parse(data);
}
