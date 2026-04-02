'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { toQueryString } from '@/lib/search-params';

export default function SearchFilters({ initialValues = {}, compact = false }) {
  const router = useRouter();
  const [city, setCity] = useState(initialValues.city ?? '');
  const [category, setCategory] = useState(initialValues.category ?? '');
  const [query, setQuery] = useState(initialValues.query ?? '');
  const [date, setDate] = useState(initialValues.date ?? '');
  const [pax, setPax] = useState(String(initialValues.pax ?? 1));

  function onSubmit(event) {
    event.preventDefault();
    const params = {
      city,
      category,
      query,
      date,
      pax
    };
    const queryString = toQueryString(params);
    router.push(`/search${queryString ? `?${queryString}` : ''}`);
  }

  return (
    <form className={`search-form ${compact ? 'compact' : ''}`} onSubmit={onSubmit}>
      <label>
        City
        <input
          type="text"
          placeholder="New York"
          value={city}
          onChange={(event) => setCity(event.target.value)}
        />
      </label>
      <label>
        Category
        <input
          type="text"
          placeholder="Museums & Galleries"
          value={category}
          onChange={(event) => setCategory(event.target.value)}
        />
      </label>
      <label>
        Keyword
        <input
          type="text"
          placeholder="MoMA"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </label>
      <label>
        Date
        <input type="date" value={date} onChange={(event) => setDate(event.target.value)} />
      </label>
      <label>
        Pax
        <input
          type="number"
          min="1"
          max="20"
          value={pax}
          onChange={(event) => setPax(event.target.value)}
        />
      </label>
      <button type="submit">{compact ? 'Update Search' : 'Compare Tickets'}</button>
    </form>
  );
}
