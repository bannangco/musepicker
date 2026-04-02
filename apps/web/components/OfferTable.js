'use client';

import Link from 'next/link';
import { useQuery } from '@tanstack/react-query';
import { buildAffiliateOutboundUrl, getActivityOffers } from '@/lib/api';
import { formatMoney } from '@/lib/format';

function groupOffers(offers) {
  const map = new Map();
  (offers ?? []).forEach((offer) => {
    const key = offer.ticketType || 'General';
    if (!map.has(key)) {
      map.set(key, []);
    }
    map.get(key).push(offer);
  });

  return [...map.entries()].map(([ticketType, grouped]) => ({
    ticketType,
    offers: [...grouped].sort((a, b) => Number(a.effectivePrice) - Number(b.effectivePrice))
  }));
}

export default function OfferTable({ activityId, date, initialOffers }) {
  const query = useQuery({
    queryKey: ['offers', activityId, date ?? null],
    queryFn: () => getActivityOffers(activityId, date ? { date } : {}),
    initialData: initialOffers
  });

  if (query.isError) {
    return (
      <section className="panel error-panel">
        <h2>Could not load offers</h2>
        <p className="muted">{query.error.message}</p>
      </section>
    );
  }

  const offers = query.data ?? [];
  if (!offers.length) {
    return (
      <section className="panel">
        <h2>Ticketed offers</h2>
        <p className="muted">No offers are currently available for this activity/date combination.</p>
      </section>
    );
  }

  const groups = groupOffers(offers);

  return (
    <section className="stack-md">
      {groups.map((group) => (
        <section key={group.ticketType} className="offer-group">
          <h3 className="offer-group-title">{group.ticketType}</h3>
          {group.offers.map((offer) => (
            <article key={offer.id} className="offer-item">
              <div className="offer-top">
                <div>
                  <p className="offer-platform">{offer.platform.name}</p>
                  <p className="offer-date">{offer.date ?? 'Flexible date'}</p>
                </div>
                <p className="offer-price">{formatMoney(offer.effectivePrice)}</p>
              </div>
              <div className="offer-footer">
                <Link
                  className="btn-primary"
                  href={buildAffiliateOutboundUrl(offer)}
                  target="_blank"
                  rel="nofollow sponsored noopener"
                >
                  View deal
                </Link>
              </div>
            </article>
          ))}
        </section>
      ))}
    </section>
  );
}
