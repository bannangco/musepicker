import SearchResultsClient from '@/components/SearchResultsClient';
import { searchActivities } from '@/lib/api';
import { titleCase } from '@/lib/format';
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
  const rawCategory = decodeSegment(params.category);
  const category = titleCase(rawCategory.replace(/-/g, ' '));
  return {
    title: `${category} Tickets | MusePicker`,
    description: `Compare ${category} ticket offers across booking platforms.`
  };
}

export default async function CategoryPage({ params, searchParams }) {
  const rawCategory = decodeSegment(params.category);
  const category = rawCategory.replace(/-/g, ' ');
  const normalized = normalizeSearchParams({ ...searchParams, category, page: searchParams?.page ?? '0' });
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
      title={`${titleCase(category)} activities`}
    />
  );
}
