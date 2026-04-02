'use client';

import { useQuery } from '@tanstack/react-query';
import ActivityCard from '@/components/ActivityCard';
import SearchFilters from '@/components/SearchFilters';
import { searchActivities } from '@/lib/api';

export default function SearchResultsClient({ normalizedParams, initialData, title }) {
  const query = useQuery({
    queryKey: ['activity-search', normalizedParams],
    queryFn: () => searchActivities(normalizedParams),
    initialData
  });

  const data = query.data;

  return (
    <section className="stack-lg">
      <header className="panel">
        <h1>{title ?? 'Search Activities'}</h1>
        <p className="muted">URL parameters are the source of truth for filters and shareable pages.</p>
        <SearchFilters initialValues={normalizedParams} compact />
      </header>

      {query.isError ? (
        <section className="panel error-panel">
          <h2>Could not load search results</h2>
          <p className="muted">{query.error.message}</p>
        </section>
      ) : null}

      <section className="results-grid" aria-live="polite">
        {(data?.items ?? []).map((item) => (
          <ActivityCard key={item.id} item={item} />
        ))}
      </section>

      <footer className="panel pagination">
        <p>
          {data?.totalElements ?? 0} activities · page {(data?.page ?? 0) + 1} / {Math.max(data?.totalPages ?? 1, 1)}
        </p>
      </footer>
    </section>
  );
}
