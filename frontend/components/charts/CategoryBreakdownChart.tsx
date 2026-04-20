"use client";

import React from "react";
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { CategoryBreakdownItem } from "@/features/analytics/types";
import { chartLabel } from "@/features/analytics/utils";

const colors = ["#4F46E5", "#7C3AED", "#06B6D4", "#10B981", "#F59E0B", "#EF4444", "#334155", "#94A3B8"];

type CategoryBreakdownChartProps = {
  items: CategoryBreakdownItem[];
};

export function CategoryBreakdownChart({ items }: CategoryBreakdownChartProps) {
  return (
    <section aria-label="Focus hours by category" className="rounded-3xl border border-line bg-white p-5 shadow-card">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold tracking-tight text-ink">Focus hours by category</h2>
          <p className="mt-1 text-sm text-muted">Where productive time is concentrated.</p>
        </div>
        <span className="rounded-full bg-cyan-50 px-3 py-1 text-xs font-semibold text-accent">{items.length} categories</span>
      </div>
      <div className="mt-5 grid gap-5 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.2fr)]">
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={items} dataKey="total_minutes" innerRadius={54} nameKey="label" outerRadius={92} paddingAngle={2}>
                {items.map((item, index) => (
                  <Cell key={item.label} fill={colors[index % colors.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value}m`, "Tracked"]} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={items} layout="vertical" margin={{ top: 8, right: 12, left: 16, bottom: 8 }}>
              <CartesianGrid stroke="#E2E8F0" strokeDasharray="4 4" horizontal={false} />
              <XAxis type="number" tick={{ fontSize: 12, fill: "#64748B" }} />
              <YAxis dataKey="label" tick={{ fontSize: 12, fill: "#64748B" }} tickFormatter={(value) => chartLabel({ label: value } as CategoryBreakdownItem)} type="category" width={96} />
              <Tooltip formatter={(value) => [`${value}m`, "Focus"]} />
              <Bar dataKey="total_minutes" fill="#06B6D4" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <ul className="mt-5 grid gap-2 text-sm sm:grid-cols-2">
          {items.map((item) => (
            <li key={item.label} className="flex items-center justify-between gap-3 rounded-2xl border border-line bg-slate-50 px-3 py-2">
              <span className="truncate font-medium text-ink" title={item.label}>
                {chartLabel(item)}
              </span>
              <span className="font-mono text-sm font-semibold text-primary">{item.display_total}</span>
            </li>
          ))}
        </ul>
    </section>
  );
}
