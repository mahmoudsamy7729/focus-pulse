import type { CategoryBreakdownItem, TagBreakdownItem } from "./types";

export function formatHoursAndMinutes(totalMinutes: number): string {
  const minutes = Math.max(0, Math.trunc(totalMinutes));
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  if (hours === 0) {
    return `${remainder}m`;
  }
  if (remainder === 0) {
    return `${hours}h`;
  }
  return `${hours}h ${remainder}m`;
}

export function todayIsoDate(): string {
  return new Date().toISOString().slice(0, 10);
}

export function chartLabel(item: CategoryBreakdownItem | TagBreakdownItem): string {
  return item.label.length > 28 ? `${item.label.slice(0, 25)}...` : item.label;
}
