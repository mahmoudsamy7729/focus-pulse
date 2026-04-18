"use client";

import React from "react";
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import type { CategoryBreakdownItem } from "@/features/analytics/types";
import { chartLabel } from "@/features/analytics/utils";

const colors = ["#0f766e", "#be123c", "#a16207", "#2563eb", "#7c2d12", "#15803d", "#b91c1c", "#0369a1"];

type CategoryBreakdownChartProps = {
  items: CategoryBreakdownItem[];
};

export function CategoryBreakdownChart({ items }: CategoryBreakdownChartProps) {
  return (
    <section aria-label="Category breakdown" className="rounded-lg border border-line bg-white p-4">
      <h2 className="text-lg font-semibold">Categories</h2>
      <div className="mt-4 grid gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(14rem,18rem)]">
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={items} dataKey="total_minutes" nameKey="label" outerRadius={88}>
                {items.map((item, index) => (
                  <Cell key={item.label} fill={colors[index % colors.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value}m`, "Tracked"]} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <ul className="grid content-start gap-2 text-sm">
          {items.map((item) => (
            <li key={item.label} className="flex items-center justify-between gap-3">
              <span className="truncate" title={item.label}>
                {chartLabel(item)}
              </span>
              <span className="font-medium text-mint">{item.display_total}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
