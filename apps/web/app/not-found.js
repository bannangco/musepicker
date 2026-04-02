import Link from 'next/link';

export default function NotFound() {
  return (
    <section className="panel stack-md">
      <h1>Activity not found</h1>
      <p className="muted">The activity may have been removed or the URL may be incorrect.</p>
      <p>
        <Link className="city-chip" href="/search">
          Return to search
        </Link>
      </p>
    </section>
  );
}
