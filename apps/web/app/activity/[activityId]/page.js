import Link from 'next/link';
import { notFound } from 'next/navigation';
import OfferTable from '@/components/OfferTable';
import SearchFilters from '@/components/SearchFilters';
import { getActivity, getActivityOffers } from '@/lib/api';

export const revalidate = 120;

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

  return (
    <section className="stack-lg">
      <section className="panel">
        <p className="eyebrow">{activity.region.city}</p>
        <h1>{activity.name}</h1>
        <p className="muted">{activity.description || 'No description yet.'}</p>
        <div className="chip-row">
          {(activity.categories ?? []).map((category) => (
            <Link key={category} className="city-chip" href={`/category/${encodeURIComponent(category)}`}>
              {category}
            </Link>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>Refine search</h2>
        <SearchFilters
          initialValues={{
            city: activity.region.city,
            category: activity.categories?.[0] ?? '',
            query: activity.name,
            date: selectedDate,
            pax: 1
          }}
          compact
        />
      </section>

      <OfferTable activityId={activityId} date={selectedDate} initialOffers={offers} />
    </section>
  );
}
