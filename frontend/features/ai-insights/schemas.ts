import { z } from "zod";

export const periodGranularitySchema = z.enum(["daily", "weekly"]);
export type PeriodGranularity = z.infer<typeof periodGranularitySchema>;

export const namedMinuteTotalSchema = z.object({
  label: z.string(),
  total_minutes: z.number().nonnegative()
});

export const dateMinuteTotalSchema = z.object({
  date: z.string(),
  total_minutes: z.number().nonnegative()
});

export const sourceSnapshotSchema = z.object({
  period_granularity: periodGranularitySchema,
  period_start: z.string(),
  period_end: z.string(),
  source_ai_insight_run_id: z.string(),
  source_daily_log_ids: z.array(z.string()).default([]),
  source_task_ids: z.array(z.string()).default([]),
  daily_log_count: z.number().nonnegative(),
  tracked_day_count: z.number().nonnegative(),
  task_count: z.number().nonnegative(),
  total_minutes: z.number().nonnegative(),
  category_totals: z.array(namedMinuteTotalSchema).default([]),
  tag_totals: z.array(namedMinuteTotalSchema).default([]),
  daily_totals: z.array(dateMinuteTotalSchema).default([]),
  phase4_observation_ids: z.array(z.string()).default([]),
  included_fields: z.array(z.string()).default([]),
  excluded_fields: z.array(z.string()).default([])
});

export const evidenceSchema = z.object({
  evidence_id: z.string(),
  evidence_type: z.string(),
  source_date: z.string().nullable().optional(),
  source_task_id: z.string().nullable().optional(),
  source_ai_insight_run_id: z.string().nullable().optional(),
  source_observation_id: z.string().nullable().optional(),
  label: z.string().nullable().optional(),
  minutes: z.number().nullable().optional(),
  count: z.number().nullable().optional(),
  summary: z.string()
});

export const scoreFactorSchema = z.object({
  label: z.string(),
  direction: z.enum(["positive", "limiting"]),
  explanation: z.string(),
  evidence_ids: z.array(z.string())
});

export const scoreOutcomeSchema = z.object({
  score_type: z.enum(["productivity", "consistency"]),
  state: z.enum(["scored", "insufficient_data", "not_applicable"]),
  score: z.number().nullable().optional(),
  confidence: z.enum(["low", "medium", "high"]),
  summary: z.string(),
  positive_factors: z.array(scoreFactorSchema).default([]),
  limiting_factors: z.array(scoreFactorSchema).default([]),
  evidence_ids: z.array(z.string()).default([]),
  insufficient_data_reason: z.string().nullable().optional()
});

export const dayFindingSchema = z.object({
  finding_type: z.enum(["best_day", "worst_day", "no_meaningful_distinction"]),
  date: z.string().nullable().optional(),
  label: z.string(),
  summary: z.string(),
  confidence: z.enum(["low", "medium", "high"]),
  evidence_ids: z.array(z.string()).default([]),
  tie_or_close_ranking: z.boolean()
});

export const recommendationSchema = z.object({
  recommendation_id: z.string(),
  priority: z.number(),
  action: z.string(),
  rationale: z.string(),
  expected_benefit: z.string(),
  confidence: z.enum(["low", "medium", "high"]),
  evidence_ids: z.array(z.string()),
  source_links: z.array(z.string()),
  dedupe_key: z.string()
});

export const validationOutcomeSchema = z.object({
  passed: z.boolean(),
  checked_at: z.string(),
  validator_version: z.string(),
  checks: z.array(z.object({ code: z.string(), passed: z.boolean(), blocking: z.boolean(), details: z.record(z.unknown()).default({}) })),
  failure_codes: z.array(z.string())
});

export const insightResultSchema = z.object({
  id: z.string(),
  status: z.enum(["completed", "failed"]),
  is_current: z.boolean(),
  generation_reason: z.enum(["default_generate", "explicit_rerun"]),
  period_granularity: periodGranularitySchema,
  period_start: z.string(),
  period_end: z.string(),
  source_ai_insight_run_id: z.string(),
  source_snapshot: sourceSnapshotSchema,
  productivity_score: scoreOutcomeSchema,
  consistency_score: scoreOutcomeSchema.nullable().optional(),
  best_day_finding: dayFindingSchema.nullable().optional(),
  worst_day_finding: dayFindingSchema.nullable().optional(),
  recommendations: z.array(recommendationSchema),
  evidence: z.array(evidenceSchema),
  validation_outcome: validationOutcomeSchema,
  failure_code: z.string().nullable().optional(),
  failure_details: z.record(z.unknown()).nullable().optional(),
  generated_at: z.string(),
  created_at: z.string()
});

export type InsightResult = z.infer<typeof insightResultSchema>;
export type ScoreOutcome = z.infer<typeof scoreOutcomeSchema>;
export type DayFinding = z.infer<typeof dayFindingSchema>;
export type Recommendation = z.infer<typeof recommendationSchema>;
export type InsightEvidence = z.infer<typeof evidenceSchema>;

export type CurrentInsightResultResponse = {
  period_granularity: PeriodGranularity;
  period_start: string;
  period_end: string;
  current_result: InsightResult | null;
};

export type InsightResultMutationResponse = {
  result: InsightResult;
  reused_existing: boolean;
};

export type InsightResultPage = {
  page: number;
  limit: number;
  total: number;
  items: InsightResult[];
};
