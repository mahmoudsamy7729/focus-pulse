import type { z } from "zod";
import type {
  categoryBreakdownItemSchema,
  dashboardOverviewSchema,
  dayDetailSchema,
  periodTypeSchema,
  tagBreakdownItemSchema
} from "./schemas";

export type PeriodType = z.infer<typeof periodTypeSchema>;
export type DashboardOverviewData = z.infer<typeof dashboardOverviewSchema>;
export type DayDetailData = z.infer<typeof dayDetailSchema>;
export type CategoryBreakdownItem = z.infer<typeof categoryBreakdownItemSchema>;
export type TagBreakdownItem = z.infer<typeof tagBreakdownItemSchema>;
