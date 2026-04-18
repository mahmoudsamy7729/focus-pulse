import { z } from "zod";

export const periodTypeSchema = z.enum(["day", "week", "month"]);

export const emptyStateSchema = z
  .object({
    code: z.string(),
    message: z.string()
  })
  .nullable();

export const namedTimeTotalSchema = z
  .object({
    label: z.string(),
    total_minutes: z.number().int().nonnegative(),
    display_total: z.string()
  })
  .nullable();

export const dashboardPeriodSchema = z.object({
  period_type: periodTypeSchema,
  anchor_date: z.string(),
  start_date: z.string(),
  end_date: z.string(),
  label: z.string()
});

export const dailyLogListItemSchema = z.object({
  date: z.string(),
  total_minutes: z.number().int().nonnegative(),
  display_total: z.string(),
  task_count: z.number().int().nonnegative(),
  top_category: namedTimeTotalSchema
});

export const periodTimeTimelinePointSchema = z.object({
  date: z.string(),
  total_minutes: z.number().int().nonnegative(),
  display_total: z.string(),
  has_tasks: z.boolean()
});

export const categoryBreakdownItemSchema = z.object({
  label: z.string(),
  total_minutes: z.number().int().nonnegative(),
  display_total: z.string(),
  share_of_total: z.number().min(0).max(1),
  is_other: z.boolean()
});

export const tagBreakdownItemSchema = z.object({
  label: z.string(),
  total_minutes: z.number().int().nonnegative(),
  display_total: z.string(),
  share_label: z.string(),
  is_untagged: z.boolean(),
  is_other: z.boolean()
});

export const dashboardSummarySchema = z.object({
  total_minutes: z.number().int().nonnegative(),
  display_total: z.string(),
  task_count: z.number().int().nonnegative(),
  daily_log_count: z.number().int().nonnegative(),
  highest_time_category: namedTimeTotalSchema,
  average_minutes_per_logged_day: z.number().int().nonnegative().nullable()
});

export const dashboardOverviewSchema = z.object({
  period: dashboardPeriodSchema,
  summary: dashboardSummarySchema,
  daily_logs: z.array(dailyLogListItemSchema),
  period_timeline: z.array(periodTimeTimelinePointSchema),
  category_breakdown: z.array(categoryBreakdownItemSchema),
  tag_breakdown: z.array(tagBreakdownItemSchema),
  tag_total_notice: z.string().nullable(),
  empty_state: emptyStateSchema
});

export const taskTimelineItemSchema = z.object({
  id: z.string().uuid(),
  title: z.string(),
  time_spent_minutes: z.number().int().positive(),
  display_time: z.string(),
  category: z.string(),
  tags: z.array(z.string()),
  note: z.string().nullable().optional(),
  source: z.string(),
  timeline_position: z.number().int().nonnegative()
});

export const dayDetailSchema = z.object({
  date: z.string(),
  total_minutes: z.number().int().nonnegative(),
  display_total: z.string(),
  task_count: z.number().int().nonnegative(),
  tasks: z.array(taskTimelineItemSchema),
  empty_state: emptyStateSchema
});
