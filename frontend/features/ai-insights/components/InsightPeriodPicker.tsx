"use client";

import React from "react";
import type { PeriodGranularity } from "../schemas";

type InsightPeriodPickerProps = {
  periodGranularity: PeriodGranularity;
  anchorDate: string;
  onPeriodGranularityChange: (periodGranularity: PeriodGranularity) => void;
  onAnchorDateChange: (anchorDate: string) => void;
};

export function InsightPeriodPicker({
  periodGranularity,
  anchorDate,
  onPeriodGranularityChange,
  onAnchorDateChange
}: InsightPeriodPickerProps) {
  return (
    <div className="grid gap-3 md:grid-cols-[180px_220px]">
      <label className="grid gap-2 text-sm font-semibold text-ink">
        Period
        <select
          className="h-11 rounded-lg border border-slate-200 bg-white px-3 text-sm font-medium text-ink"
          value={periodGranularity}
          onChange={(event) => onPeriodGranularityChange(event.target.value as PeriodGranularity)}
        >
          <option value="daily">Day</option>
          <option value="weekly">Week</option>
        </select>
      </label>
      <label className="grid gap-2 text-sm font-semibold text-ink">
        Anchor date
        <input
          className="h-11 rounded-lg border border-slate-200 bg-white px-3 text-sm font-medium text-ink"
          type="date"
          value={anchorDate}
          onChange={(event) => onAnchorDateChange(event.target.value)}
        />
      </label>
    </div>
  );
}
