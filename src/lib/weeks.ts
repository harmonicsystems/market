import { getCollection, type CollectionEntry } from 'astro:content';

export type WeekEntry = CollectionEntry<'weeks'>;

/**
 * Today's date in America/New_York as an ISO string (YYYY-MM-DD).
 * Used for selecting the next market — must be ET, not UTC, because the
 * site builds on a UTC server but lives on a Saturday market in NY.
 */
export function todayInET(now: Date = new Date()): string {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/New_York',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(now);
  const y = parts.find((p) => p.type === 'year')!.value;
  const m = parts.find((p) => p.type === 'month')!.value;
  const d = parts.find((p) => p.type === 'day')!.value;
  return `${y}-${m}-${d}`;
}

/** All weeks, sorted ascending by date. */
export async function getAllWeeks(): Promise<WeekEntry[]> {
  const all = await getCollection('weeks');
  return all.sort((a, b) => a.data.date.localeCompare(b.data.date));
}

/**
 * The "Next Market" week — first week whose date is today or in the future
 * (ET). Returns undefined when no future market is on the books (the season
 * has wrapped, or weeks haven't been seeded yet). Callers should render an
 * off-season message in that case.
 */
export async function getCurrentMarketWeek(): Promise<WeekEntry | undefined> {
  const weeks = await getAllWeeks();
  if (weeks.length === 0) return undefined;
  const today = todayInET();
  return weeks.find((w) => w.data.date >= today);
}

/** Format an ISO date as "Saturday, May 9, 2026" — used everywhere displayDate appears. */
export function formatDisplayDate(iso: string): string {
  return new Date(iso + 'T12:00:00').toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    timeZone: 'America/New_York',
  });
}
