import Link from 'next/link';
import SearchFilters from '@/components/SearchFilters';
import { formatMoney } from '@/lib/format';
import { getRegionCities, getTrendingActivities } from '@/lib/api';

export const dynamic = 'force-dynamic';

export default async function HomePage() {
  let cities = [];
  let trending = [];
  try {
    [cities, trending] = await Promise.all([getRegionCities(), getTrendingActivities()]);
  } catch {
    cities = [];
    trending = [];
  }

  return (
    <section className="stack-xl">
      <section className="hero-card">
        <p className="eyebrow">Flip & Compare Tickets</p>
        <h1>Find the best cultural ticket prices in one place.</h1>
        <p className="muted">
          Search city-first, compare top partner prices quickly, and continue to booking through tracked affiliate links.
        </p>
        <SearchFilters initialValues={{ pax: 1 }} />
      </section>

      <section className="panel stack-md">
        <div className="section-head">
          <h2>Where are you going?</h2>
          <Link href="/search">See all cities</Link>
        </div>

        <div className="city-grid">
          {(cities ?? []).map((city) => (
            <article key={city.id} className="city-card">
              <div className="city-cover">
                <h3>
                  {city.city}
                  {city.state ? `, ${city.state}` : ''}
                </h3>
                <p className="city-meta">{city.totalCount} things to do</p>
              </div>
              <div className="city-body">
                <div className="chip-row">
                  {(city.categories ?? []).slice(0, 3).map((category) => (
                    <span key={`${city.id}-${category}`} className="city-chip">
                      {category}
                    </span>
                  ))}
                </div>
                <div className="city-foot">
                  <p className="city-price">from {formatMoney(city.lowestPrice)}</p>
                  <Link className="btn-primary" href={`/city/${encodeURIComponent(city.city)}`}>
                    Explore City
                  </Link>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="panel stack-md">
        <div className="section-head">
          <h2>Trending Tickets</h2>
          <Link href="/search">Browse all</Link>
        </div>
        <div className="trend-rail">
          {(trending ?? []).map((item) => (
            <article key={item.id} className="trend-card">
              <div
                className="trend-image"
                style={
                  item.image
                    ? {
                        backgroundImage: `linear-gradient(180deg, rgba(11, 32, 68, 0.15), rgba(11, 32, 68, 0.92)), url(${item.image})`,
                        backgroundSize: 'cover',
                        backgroundPosition: 'center'
                      }
                    : undefined
                }
              />
              <div className="trend-body">
                <h3>{item.name}</h3>
                <p className="trend-price">from {formatMoney(item.lowestPrice)}</p>
                <Link className="btn-secondary" href={`/activity/${item.id}`}>
                  View deal
                </Link>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="petition-card">
        <h2>Want another city on MusePicker?</h2>
        <p className="muted">
          Tell us which city you want next. We use requests to prioritize source integration and curation.
        </p>
        <Link
          className="btn-petition"
          href="mailto:yunboshim@gmail.com?subject=MusePicker%20City%20Request&body=Please%20add%20this%20city:%20"
        >
          + Petition for More Cities
        </Link>
      </section>
    </section>
  );
}
