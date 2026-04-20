"use client";

import React from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { TagBreakdownItem } from "@/features/analytics/types";
import { chartLabel } from "@/features/analytics/utils";

type TagBreakdownChartProps = {
  items: TagBreakdownItem[];
  notice?: string | null;
};

export function TagBreakdownChart({ items, notice }: TagBreakdownChartProps) {
  return (
    <section aria-label="Task completion breakdown" className="rounded-3xl border border-line bg-white p-5 shadow-card">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold tracking-tight text-ink">Task completion breakdown</h2>
          <p className="mt-1 text-sm text-muted">Completion signals grouped by tags and imported task labels.</p>
        </div>
        {notice ? <p className="max-w-md rounded-2xl bg-warning/10 px-3 py-2 text-sm text-warning">{notice}</p> : null}
      </div>
      <div className="mt-5 h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={items} layout="vertical" margin={{ top: 8, right: 12, left: 20, bottom: 8 }}>
            <CartesianGrid stroke="#E2E8F0" strokeDasharray="4 4" horizontal={false} />
            <XAxis type="number" tick={{ fontSize: 12, fill: "#64748B" }} />
            <YAxis dataKey="label" type="category" tick={{ fontSize: 12, fill: "#64748B" }} tickFormatter={(value) => chartLabel({ label: value } as TagBreakdownItem)} width={96} />
            <Tooltip formatter={(value) => [`${value}m`, "Counted"]} />
            <Bar dataKey="total_minutes" fill="#7C3AED" radius={[0, 8, 8, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <ul className="mt-5 grid gap-2 text-sm sm:grid-cols-2">
        {items.map((item) => (
          <li key={item.label} className="flex items-center justify-between gap-3 rounded-2xl border border-line bg-slate-50 px-3 py-2">
            <span className="truncate font-medium text-ink" title={item.label}>
              {chartLabel(item)}
            </span>
            <span className="font-mono text-sm font-semibold text-secondary">{item.display_total}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
