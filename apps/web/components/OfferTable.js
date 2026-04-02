'use client';

import Link from 'next/link';
import { useQuery } from '@tanstack/react-query';
import { formatMoney } from '@/lib/format';
import { buildAffiliateOutboundUrl, getActivityOffers } from '@/lib/api';

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
        <h2>Offers</h2>
        <p className="muted">No offers are currently available for this activity/date combination.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <h2>Offers</h2>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Platform</th>
              <th>Ticket Type</th>
              <th>Date</th>
              <th>Effective Price</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {offers.map((offer) => (
              <tr key={offer.id}>
                <td>{offer.platform.name}</td>
                <td>{offer.ticketType}</td>
                <td>{offer.date ?? '-'}</td>
                <td>{formatMoney(offer.effectivePrice)}</td>
                <td>
                  <Link
                    className="outbound"
                    href={buildAffiliateOutboundUrl(offer)}
                    target="_blank"
                    rel="nofollow sponsored noopener"
                  >
                    Go to booking
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
