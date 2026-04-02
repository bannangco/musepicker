import SearchResultsClient from '@/components/SearchResultsClient';
import { searchActivities } from '@/lib/api';
import { normalizeSearchParams } from '@/lib/search-params';

export const revalidate = 180;

function decodeSegment(value) {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
}

export async function generateMetadata({ params }) {
  const city = decodeSegment(params.city);
  return {
    title: `${city} Tickets | MusePicker`,
    description: `Compare museum, gallery, and attraction ticket offers in ${city}.`
  };
}

export default async function CityPage({ params, searchParams }) {
  const city = decodeSegment(params.city);
  const normalized = normalizeSearchParams({ ...searchParams, city, page: searchParams?.page ?? '0' });
  let initialData = {
    page: normalized.page,
    size: normalized.size,
    totalElements: 0,
    totalPages: 0,
    items: []
  };
  try {
    initialData = await searchActivities(normalized, { cache: 'force-cache', revalidate: 180 });
  } catch {
    // Graceful fallback when API is unavailable at render time.
  }

  return (
    <SearchResultsClient
      normalizedParams={normalized}
      initialData={initialData}
      title={`Top activities in ${city}`}
    />
  );
}
