'use client';

import Link from 'next/link';
import { useQuery } from '@tanstack/react-query';
import { useMemo, useState } from 'react';
import SearchFilters from '@/components/SearchFilters';
import { formatMoney } from '@/lib/format';
import { searchActivities } from '@/lib/api';

function priceOf(ticket) {
  const value = Number(ticket?.price);
  return Number.isFinite(value) ? value : Number.POSITIVE_INFINITY;
}

function cheapestOf(item) {
  const preview = item.ticketPreview ?? [];
  if (!preview.length) {
    return Number.POSITIVE_INFINITY;
  }
  return Math.min(...preview.map((ticket) => priceOf(ticket)));
}

function discountScore(item) {
  const preview = item.ticketPreview ?? [];
  if (preview.length < 2) {
    return 0;
  }
  const prices = preview.map((ticket) => priceOf(ticket)).filter((value) => Number.isFinite(value));
  if (prices.length < 2) {
    return 0;
  }
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  if (max <= 0) {
    return 0;
  }
  return (max - min) / max;
}

function sortItems(items, sortBy) {
  const copy = [...items];
  if (sortBy === 'price_desc') {
    return copy.sort((a, b) => cheapestOf(b) - cheapestOf(a));
  }
  if (sortBy === 'best_discount') {
    return copy.sort((a, b) => discountScore(b) - discountScore(a));
  }
  return copy.sort((a, b) => cheapestOf(a) - cheapestOf(b));
}

function makeHref(pathname, params) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value === '' || value === null || value === undefined) {
      return;
    }
    query.set(key, String(value));
  });
  const queryText = query.toString();
  return queryText ? `${pathname}?${queryText}` : pathname;
}

export default function SearchResultsClient({ normalizedParams, initialData, title }) {
  const [sortBy, setSortBy] = useState('price_asc');
  const query = useQuery({
    queryKey: ['activity-search', normalizedParams],
    queryFn: () => searchActivities(normalizedParams),
    initialData
  });

  const data = query.data;
  const sortedItems = useMemo(() => sortItems(data?.items ?? [], sortBy), [data?.items, sortBy]);
  const currentPage = data?.page ?? normalizedParams.page ?? 0;
  const totalPages = Math.max(data?.totalPages ?? 0, 1);

  const prevHref = makeHref('/search', { ...normalizedParams, page: Math.max(currentPage - 1, 0) });
  const nextHref = makeHref('/search', { ...normalizedParams, page: currentPage + 1 });

  return (
    <section className="stack-lg">
      <header className="sticky-filters">
        <h1>{title ?? 'Search Activities'}</h1>
        <p className="muted">Compare offers by city, category, date, and passenger count.</p>
        <SearchFilters initialValues={normalizedParams} compact />
        <div className="sort-row">
          <label htmlFor="sort-select">Sort</label>
          <select id="sort-select" value={sortBy} onChange={(event) => setSortBy(event.target.value)}>
            <option value="price_asc">Price low to high</option>
            <option value="price_desc">Price high to low</option>
            <option value="best_discount">Best discount</option>
          </select>
        </div>
      </header>

      {query.isError ? (
        <section className="panel error-panel">
          <h2>Could not load search results</h2>
          <p className="muted">{query.error.message}</p>
        </section>
      ) : null}

      <section className="results-grid" aria-live="polite">
        {sortedItems.map((item) => {
          const preview = item.ticketPreview ?? [];
          const topPreview = preview.slice(0, 2);
          const moreCount = Math.max(preview.length - 2, 0);
          const firstPrice = Number.isFinite(cheapestOf(item)) ? cheapestOf(item) : null;
          const activityHref = makeHref(`/activity/${item.id}`, {
            date: normalizedParams.date || undefined
          });

          return (
            <article className="result-card" key={item.id}>
              <div
                className="result-media"
                style={
                  item.image
                    ? {
                        backgroundImage: `linear-gradient(180deg, rgba(8, 29, 72, 0.2), rgba(8, 29, 72, 0.9)), url(${item.image})`,
                        backgroundSize: 'cover',
                        backgroundPosition: 'center'
                      }
                    : undefined
                }
              />
              <div className="result-body">
                <div className="result-header">
                  <h2 className="result-title">
                    <Link href={activityHref}>{item.name}</Link>
                  </h2>
                  <p className="result-meta">
                    {item.city}
                    {item.state ? `, ${item.state}` : ''} · {item.platformCount} platforms · {item.ticketTypeCount} ticket
                    types
                  </p>
                </div>

                <ul className="preview-list">
                  {topPreview.map((ticket) => (
                    <li key={`${item.id}-${ticket.platformName}-${ticket.price}`}>
                      <span>{ticket.platformName}</span>
                      <strong>{formatMoney(ticket.price)}</strong>
                    </li>
                  ))}
                </ul>

                {moreCount > 0 ? <p className="preview-more">Quickly and {moreCount} more seller options</p> : null}

                <div className="result-actions">
                  <p className="result-price">{firstPrice === null ? '-' : `from ${formatMoney(firstPrice)}`}</p>
                  <Link href={activityHref} className="btn-primary">
                    View Prices
                  </Link>
                </div>
              </div>
            </article>
          );
        })}
      </section>

      {!query.isError && sortedItems.length === 0 ? (
        <section className="panel">
          <h2>No matching activities</h2>
          <p className="muted">Try a different city, category, or date to see available ticket comparisons.</p>
        </section>
      ) : null}

      <footer className="panel pagination-bar">
        <p>
          {data?.totalElements ?? 0} activities · page {currentPage + 1} / {totalPages}
        </p>
        <div className="chip-row">
          <Link className="btn-secondary" href={prevHref} aria-disabled={currentPage <= 0}>
            Prev
          </Link>
          <Link className="btn-secondary" href={nextHref} aria-disabled={currentPage + 1 >= totalPages}>
            Next
          </Link>
        </div>
      </footer>
    </section>
  );
}
