import Link from 'next/link';
import ActivityCard from '@/components/ActivityCard';
import SearchFilters from '@/components/SearchFilters';
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

  const trendingAsCards = (trending ?? []).map((item) => ({
    id: item.id,
    name: item.name,
    city: 'Trending',
    ticketTypeCount: 0,
    platformCount: 0,
    ticketPreview: [{ platformName: 'Best price', price: item.lowestPrice }]
  }));

  return (
    <section className="stack-xl">
      <section className="hero panel">
        <p className="eyebrow">Metasearch For Cultural Tickets</p>
        <h1>Compare activity ticket prices across platforms in one search.</h1>
        <p className="muted">
          MusePicker unifies offers from Klook, Viator, Trip.com, TicketsToDo and more, then ranks by effective price.
        </p>
        <SearchFilters initialValues={{ pax: 1 }} />
      </section>

      <section className="panel stack-md">
        <div className="section-head">
          <h2>Trending activities</h2>
          <Link href="/search">See all</Link>
        </div>
        <div className="results-grid">
          {trendingAsCards.map((item) => (
            <ActivityCard key={item.id} item={item} />
          ))}
        </div>
      </section>

      <section className="panel stack-md">
        <div className="section-head">
          <h2>Browse by city</h2>
        </div>
        <div className="chip-row">
          {(cities ?? []).map((city) => (
            <Link className="city-chip" key={city.id} href={`/city/${encodeURIComponent(city.city)}`}>
              <span>{city.city}</span>
              <span>{city.totalCount} activities</span>
            </Link>
          ))}
        </div>
      </section>
    </section>
  );
}
