"use client";

import React from "react";
import { useEffect, useMemo, useState } from "react";
import { CategoryBreakdownChart } from "@/components/charts/CategoryBreakdownChart";
import { PeriodTimeTimeline } from "@/components/charts/PeriodTimeTimeline";
import { TagBreakdownChart } from "@/components/charts/TagBreakdownChart";
import { DashboardShell } from "@/components/layout/DashboardShell";
import { useDashboardOverview } from "../hooks";
import type { PeriodType } from "../types";
import { todayIsoDate } from "../utils";
import { AIInsightsPanel } from "./AIInsightsPanel";
import { DailyLogsList } from "./DailyLogsList";
import { DashboardFilters } from "./DashboardFilters";
import { DayDetailView } from "./DayDetailView";
import { EmptyState } from "./EmptyState";
import { SummaryCards } from "./SummaryCards";
import { TasksTable } from "./TasksTable";
import { WeeklyActivityHeatmap } from "./WeeklyActivityHeatmap";

export function DashboardOverview() {
  const [periodType, setPeriodType] = useState<PeriodType>("day");
  const [anchorDate, setAnchorDate] = useState<string | undefined>(undefined);
  const [selectedDate, setSelectedDate] = useState<string | undefined>(undefined);
  const dashboardQuery = useDashboardOverview(periodType, anchorDate);
  const visibleAnchorDate = anchorDate ?? dashboardQuery.data?.period.anchor_date ?? todayIsoDate();

  useEffect(() => {
    if (!selectedDate && dashboardQuery.data?.daily_logs[0]?.date) {
      setSelectedDate(dashboardQuery.data.daily_logs[0].date);
    }
  }, [dashboardQuery.data, selectedDate]);

  const showTimeline = useMemo(() => dashboardQuery.data?.period_timeline ?? [], [dashboardQuery.data]);

  return (
    <DashboardShell>
      <DashboardFilters
        periodType={periodType}
        anchorDate={visibleAnchorDate}
        onPeriodTypeChange={(nextPeriod) => {
          setPeriodType(nextPeriod);
          setSelectedDate(undefined);
        }}
        onAnchorDateChange={(nextDate) => {
          setAnchorDate(nextDate);
          setSelectedDate(undefined);
        }}
      />

      {dashboardQuery.isLoading ? (
        <div className="rounded-3xl border border-line bg-white p-6 text-sm text-muted shadow-card">Loading dashboard...</div>
      ) : null}

      {dashboardQuery.isError ? (
        <EmptyState title="Dashboard unavailable" message="The dashboard data could not be loaded." />
      ) : null}

      {dashboardQuery.data ? (
        <>
          <SummaryCards summary={dashboardQuery.data.summary} />
          {dashboardQuery.data.empty_state ? <EmptyState message={dashboardQuery.data.empty_state.message} /> : null}
          <div className="grid gap-6 xl:grid-cols-[minmax(0,1.7fr)_minmax(24rem,0.8fr)]">
            <div className="grid min-w-0 gap-6">
              <PeriodTimeTimeline points={showTimeline} />
              <div className="grid gap-6 2xl:grid-cols-2">
                <CategoryBreakdownChart items={dashboardQuery.data.category_breakdown} />
                <TagBreakdownChart items={dashboardQuery.data.tag_breakdown} notice={dashboardQuery.data.tag_total_notice} />
              </div>
              <WeeklyActivityHeatmap logs={dashboardQuery.data.daily_logs} />
              <TasksTable selectedDate={selectedDate} />
            </div>
            <div className="grid min-w-0 content-start gap-6">
              <AIInsightsPanel summary={dashboardQuery.data.summary} />
              <DailyLogsList
                logs={dashboardQuery.data.daily_logs}
                selectedDate={selectedDate}
                onSelectDate={setSelectedDate}
              />
              <DayDetailView selectedDate={selectedDate} />
            </div>
          </div>
        </>
      ) : null}
    </DashboardShell>
  );
}
