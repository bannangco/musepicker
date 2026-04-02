import Link from 'next/link';
import { formatMoney } from '@/lib/format';
import { normalizeSearchParams, toQueryString } from '@/lib/search-params';
import { searchActivities } from '@/lib/api';

export const revalidate = 180;

const REGION_CATEGORIES = [
  { icon: '🏛️', label: 'Museums', value: 'Museums & Galleries' },
  { icon: '🎡', label: 'Amusement', value: 'Amusement' },
  { icon: '🧒', label: 'Kids', value: 'Kids Activities' },
  { icon: '🎭', label: 'Art & Theater', value: 'Art & Theater' },
  { icon: '💆', label: 'Beauty & Spa', value: 'Beauty & Spa' },
  { icon: '🧭', label: 'All Categories', value: '' }
];

const PROMOS = [
  {
    badge: 'Deal',
    title: 'Find shows and museums with the strongest discounts in one list.'
  },
  {
    badge: 'Partner',
    title: 'Compare Klook, Viator, Trip.com, and more offers at once.'
  },
  {
    badge: 'Quick',
    title: 'Filter by date and pax to see price-ready options instantly.'
  }
];

function decodeSegment(value) {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
}

function makeCityHref(city, params = {}) {
  const query = toQueryString(params);
  const path = `/city/${encodeURIComponent(city)}`;
  return query ? `${path}?${query}` : path;
}

function activityHref(itemId, date) {
  if (!date) {
    return `/activity/${itemId}`;
  }
  return `/activity/${itemId}?${toQueryString({ date })}`;
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
  const normalized = normalizeSearchParams({
    ...searchParams,
    city,
    page: searchParams?.page ?? '0',
    size: searchParams?.size ?? '5'
  });

  let result = {
    page: normalized.page,
    size: normalized.size,
    totalElements: 0,
    totalPages: 0,
    items: []
  };
  try {
    result = await searchActivities(normalized, { cache: 'force-cache', revalidate: 180 });
  } catch {
    result = {
      page: normalized.page,
      size: normalized.size,
      totalElements: 0,
      totalPages: 0,
      items: []
    };
  }

  const nextPageParams = {
    query: normalized.query,
    category: normalized.category,
    date: normalized.date,
    pax: normalized.pax,
    size: normalized.size,
    page: (result.page ?? 0) + 1
  };
  const hasMore = (result.page ?? 0) + 1 < (result.totalPages ?? 0);

  return (
    <section className="stack-lg">
      <section className="city-hero">
        <p className="breadcrumb">Home &gt; {city}</p>
        <h1>{city}</h1>
        <form className="city-search-local" action="/search">
          <input type="hidden" name="city" value={city} />
          <input type="text" name="query" defaultValue={normalized.query} placeholder={`Search things to do in ${city}`} />
          <button type="submit">Search</button>
        </form>
      </section>

      <section className="panel stack-md">
        <h2>Categories</h2>
        <div className="category-grid">
          {REGION_CATEGORIES.map((category) => (
            <Link
              key={`${category.label}-${category.value || 'all'}`}
              className="category-pill"
              href={`/search?${toQueryString({
                city,
                category: category.value || undefined,
                date: normalized.date || undefined,
                pax: normalized.pax || 1
              })}`}
            >
              <span className="emoji">{category.icon}</span>
              <span>{category.label}</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="panel stack-md">
        <h2>Find shows in {city}</h2>
        <div className="promo-rail">
          {PROMOS.map((promo) => (
            <article key={promo.title} className="promo-card">
              <span className="promo-badge">{promo.badge}</span>
              <h3>{promo.title}</h3>
            </article>
          ))}
        </div>
      </section>

      <section className="panel stack-md">
        <div className="section-head">
          <h2>Popular Tickets in {city}</h2>
        </div>
        <form className="search-form compact" action={makeCityHref(city)}>
          <input type="hidden" name="query" value={normalized.query || ''} />
          <input type="hidden" name="category" value={normalized.category || ''} />
          <input type="hidden" name="size" value={normalized.size} />
          <label>
            Date
            <input type="date" name="date" defaultValue={normalized.date} />
          </label>
          <label>
            Pax
            <input type="number" min="1" max="20" name="pax" defaultValue={normalized.pax} />
          </label>
          <button type="submit">Update Search</button>
        </form>

        <section className="results-grid">
          {(result.items ?? []).map((item) => {
            const preview = item.ticketPreview ?? [];
            const topPreview = preview.slice(0, 2);
            const moreCount = Math.max(preview.length - 2, 0);
            const firstPrice = topPreview.length ? topPreview[0].price : null;
            const href = activityHref(item.id, normalized.date);

            return (
              <article key={item.id} className="result-card">
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
                    <h3 className="result-title">
                      <Link href={href}>{item.name}</Link>
                    </h3>
                    <p className="result-meta">
                      {item.city}
                      {item.state ? `, ${item.state}` : ''} · {item.platformCount} platforms
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
                    <Link href={href} className="btn-primary">
                      View Prices
                    </Link>
                  </div>
                </div>
              </article>
            );
          })}
        </section>

        {hasMore ? (
          <p>
            <Link className="btn-secondary" href={makeCityHref(city, nextPageParams)}>
              + Show more results
            </Link>
          </p>
        ) : null}
      </section>
    </section>
  );
}
