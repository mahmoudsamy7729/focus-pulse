import React from "react";

type EmptyStateProps = {
  title?: string;
  message: string;
};

export function EmptyState({ title = "Nothing tracked here yet", message }: EmptyStateProps) {
  return (
    <div className="rounded-lg border border-dashed border-line bg-white p-6 text-sm text-gray-700" role="status">
      <p className="font-medium text-ink">{title}</p>
      <p className="mt-1">{message}</p>
    </div>
  );
}
