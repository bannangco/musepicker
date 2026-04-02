import Link from 'next/link';
import { notFound } from 'next/navigation';
import OfferTable from '@/components/OfferTable';
import { formatMoney } from '@/lib/format';
import { getActivity, getActivityOffers, getTrendingActivities, searchActivities } from '@/lib/api';
import { toQueryString } from '@/lib/search-params';

export const revalidate = 120;

function nearbyHref(itemId, date) {
  if (!date) {
    return `/activity/${itemId}`;
  }
  return `/activity/${itemId}?${toQueryString({ date })}`;
}

export async function generateMetadata({ params }) {
  try {
    const activity = await getActivity(params.activityId, { cache: 'force-cache', revalidate: 120 });
    return {
      title: `${activity.name} | MusePicker`,
      description: activity.description || `Compare ${activity.name} ticket offers from multiple platforms.`
    };
  } catch {
    return {
      title: 'Activity | MusePicker'
    };
  }
}

export default async function ActivityPage({ params, searchParams }) {
  const activityId = params.activityId;
  const selectedDate = searchParams?.date ?? '';
  const selectedPax = searchParams?.pax ?? '1';

  let activity;
  try {
    activity = await getActivity(activityId, { cache: 'force-cache', revalidate: 120 });
  } catch {
    notFound();
  }

  let offers = [];
  try {
    offers = await getActivityOffers(
      activityId,
      selectedDate ? { date: selectedDate } : {},
      { cache: 'force-cache', revalidate: 120 }
    );
  } catch {
    offers = [];
  }

  let nearbyItems = [];
  let trending = [];
  try {
    const nearby = await searchActivities(
      {
        city: activity.region.city,
        category: '',
        query: '',
        date: selectedDate,
        pax: Number(selectedPax) || 1,
        page: 0,
        size: 6
      },
      { cache: 'force-cache', revalidate: 120 }
    );
    nearbyItems = (nearby?.items ?? []).filter((item) => item.id !== activity.id).slice(0, 6);
    trending = await getTrendingActivities({ cache: 'force-cache', revalidate: 120 });
  } catch {
    nearbyItems = [];
    trending = [];
  }

  const bestPrice = offers.length
    ? Math.min(...offers.map((offer) => Number(offer.effectivePrice)).filter((value) => Number.isFinite(value)))
    : null;

  return (
    <section className="stack-lg">
      <section className="detail-hero">
        <div
          className="detail-cover"
          style={
            activity.images?.[0]
              ? {
                  backgroundImage: `linear-gradient(180deg, rgba(13, 24, 51, 0.18), rgba(13, 24, 51, 0.88)), url(${activity.images[0]})`,
                  backgroundSize: 'cover',
                  backgroundPosition: 'center'
                }
              : undefined
          }
        >
          <div className="detail-head">
            <p className="breadcrumb">
              Home &gt; {activity.region.city} &gt; {activity.name}
            </p>
            <h1>{activity.name}</h1>
            <p>{activity.region.city}</p>
          </div>
        </div>
        <div className="detail-content stack-md">
          <p className="muted">{activity.description || 'No description yet.'}</p>
          <div className="detail-pill-row">
            {(activity.categories ?? []).map((category) => (
              <Link key={category} className="city-chip" href={`/category/${encodeURIComponent(category)}`}>
                {category}
              </Link>
            ))}
          </div>
          <form className="search-form compact" action={`/activity/${activity.id}`}>
            <label>
              Date
              <input type="date" name="date" defaultValue={selectedDate} />
            </label>
            <label>
              Pax
              <input type="number" min="1" max="20" name="pax" defaultValue={selectedPax} />
            </label>
            <button type="submit">Update Search</button>
          </form>
          <p className="callout">
            {bestPrice === null ? 'No live price available right now.' : `Best current price: ${formatMoney(bestPrice)}`}
          </p>
        </div>
      </section>

      <section className="panel stack-md">
        <h2>Ticketed Exhibitions</h2>
        <OfferTable activityId={activityId} date={selectedDate} initialOffers={offers} />
      </section>

      <section className="placeholder-grid">
        <section className="panel stack-md">
          <h2>Location</h2>
          <div className="map-placeholder">
            <div>
              <p>Interactive map placeholder</p>
              <p>
                {activity.region.city}
                {activity.region.state ? `, ${activity.region.state}` : ''}
              </p>
            </div>
          </div>
          <p className="muted">Coordinates and full venue map integrations will be added in the next API phase.</p>
        </section>

        <section className="panel stack-md">
          <h2>What&apos;s nearby</h2>
          <p className="callout">Nearby points of interest and route estimates are coming soon.</p>
        </section>

        <section className="panel stack-md">
          <h2>Guest Reviews</h2>
          <p className="callout">Structured review aggregation is coming soon.</p>
        </section>
      </section>

      <section className="panel stack-md">
        <div className="section-head">
          <h2>Nearby Tickets</h2>
          <Link href={`/search?${toQueryString({ city: activity.region.city })}`}>See more</Link>
        </div>
        <div className="trend-rail">
          {(nearbyItems.length ? nearbyItems : trending).map((item) => {
            const price = item.lowestPrice ?? item.ticketPreview?.[0]?.price;
            const name = item.name;
            const image = item.image;
            return (
              <article key={item.id} className="trend-card">
                <div
                  className="trend-image"
                  style={
                    image
                      ? {
                          backgroundImage: `linear-gradient(180deg, rgba(11, 32, 68, 0.15), rgba(11, 32, 68, 0.92)), url(${image})`,
                          backgroundSize: 'cover',
                          backgroundPosition: 'center'
                        }
                      : undefined
                  }
                />
                <div className="trend-body">
                  <h3>{name}</h3>
                  <p className="trend-price">{price === undefined ? '-' : `from ${formatMoney(price)}`}</p>
                  <Link className="btn-secondary" href={nearbyHref(item.id, selectedDate)}>
                    View tickets
                  </Link>
                </div>
              </article>
            );
          })}
        </div>
      </section>
    </section>
  );
}
