import SearchResultsClient from '@/components/SearchResultsClient';
import { searchActivities } from '@/lib/api';
import { normalizeSearchParams } from '@/lib/search-params';

export const revalidate = 120;

export const metadata = {
  title: 'Search Activities | MusePicker',
  description: 'Search city/category/activity tickets and compare live offers across platforms.'
};

export default async function SearchPage({ searchParams }) {
  const normalized = normalizeSearchParams(searchParams);
  let initialData = {
    page: normalized.page,
    size: normalized.size,
    totalElements: 0,
    totalPages: 0,
    items: []
  };
  try {
    initialData = await searchActivities(normalized, { cache: 'force-cache', revalidate: 120 });
  } catch {
    // Graceful fallback when API is unavailable at render time.
  }

  return <SearchResultsClient normalizedParams={normalized} initialData={initialData} />;
}
