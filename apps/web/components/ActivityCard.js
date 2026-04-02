import Link from 'next/link';
import { formatMoney } from '@/lib/format';

export default function ActivityCard({ item }) {
  const cheapest = item.ticketPreview?.[0]?.price;

  return (
    <article className="activity-card">
      <div className="activity-topline">
        <p className="activity-city">{item.city}</p>
        <p className="activity-cheapest">from {formatMoney(cheapest)}</p>
      </div>
      <h3>
        <Link href={`/activity/${item.id}`}>{item.name}</Link>
      </h3>
      <p className="activity-meta">
        {item.platformCount} platforms · {item.ticketTypeCount} ticket types
      </p>
      <ul>
        {(item.ticketPreview ?? []).map((ticket) => (
          <li key={`${ticket.platformName}-${ticket.price}`}>
            <span>{ticket.platformName}</span>
            <span>{formatMoney(ticket.price)}</span>
          </li>
        ))}
      </ul>
    </article>
  );
}
