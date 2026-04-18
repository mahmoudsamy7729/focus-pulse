import React from "react";
import type { PeriodType } from "../types";

type DashboardFiltersProps = {
  periodType: PeriodType;
  anchorDate: string;
  onPeriodTypeChange: (periodType: PeriodType) => void;
  onAnchorDateChange: (anchorDate: string) => void;
};

const periodOptions: { value: PeriodType; label: string }[] = [
  { value: "day", label: "Day" },
  { value: "week", label: "Week" },
  { value: "month", label: "Month" }
];

export function DashboardFilters({
  periodType,
  anchorDate,
  onPeriodTypeChange,
  onAnchorDateChange
}: DashboardFiltersProps) {
  return (
    <div className="flex flex-col gap-3 border-b border-line pb-5 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <h1 className="text-3xl font-semibold">Dashboard</h1>
        <p className="mt-2 max-w-2xl text-sm text-gray-600">
          Track the day, compare the week, and inspect the work behind the totals.
        </p>
      </div>
      <div className="flex flex-wrap items-end gap-3">
        <label className="grid gap-1 text-sm font-medium text-gray-700">
          Period
          <select
            className="focus-ring h-10 rounded-md border border-line bg-white px-3 text-ink"
            value={periodType}
            onChange={(event) => onPeriodTypeChange(event.target.value as PeriodType)}
          >
            {periodOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>
        <label className="grid gap-1 text-sm font-medium text-gray-700">
          Anchor date
          <input
            className="focus-ring h-10 rounded-md border border-line bg-white px-3 text-ink"
            type="date"
            value={anchorDate}
            onChange={(event) => onAnchorDateChange(event.target.value)}
          />
        </label>
      </div>
    </div>
  );
}
