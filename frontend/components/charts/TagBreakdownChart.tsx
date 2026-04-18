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
    <section aria-label="Tag breakdown" className="rounded-lg border border-line bg-white p-4">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <h2 className="text-lg font-semibold">Tags</h2>
        {notice ? <p className="max-w-md text-sm text-amber">{notice}</p> : null}
      </div>
      <div className="mt-4 h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={items} layout="vertical" margin={{ top: 8, right: 12, left: 20, bottom: 8 }}>
            <CartesianGrid stroke="#e5e7eb" horizontal={false} />
            <XAxis type="number" tick={{ fontSize: 12 }} />
            <YAxis dataKey="label" type="category" tickFormatter={(value) => chartLabel({ label: value } as TagBreakdownItem)} width={96} />
            <Tooltip formatter={(value) => [`${value}m`, "Counted"]} />
            <Bar dataKey="total_minutes" fill="#be123c" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <ul className="mt-4 grid gap-2 text-sm sm:grid-cols-2">
        {items.map((item) => (
          <li key={item.label} className="flex items-center justify-between gap-3">
            <span className="truncate" title={item.label}>
              {chartLabel(item)}
            </span>
            <span className="font-medium text-coral">{item.display_total}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
