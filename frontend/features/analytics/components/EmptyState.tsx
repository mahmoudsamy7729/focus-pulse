import React from "react";

type EmptyStateProps = {
  title?: string;
  message: string;
};

export function EmptyState({ title = "Nothing tracked here yet", message }: EmptyStateProps) {
  return (
    <div className="rounded-3xl border border-dashed border-line bg-white p-6 text-sm text-muted shadow-card" role="status">
      <p className="font-semibold text-ink">{title}</p>
      <p className="mt-1 leading-6">{message}</p>
    </div>
  );
}
