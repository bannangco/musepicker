import {
  getMappingReviewQueue,
  getOfferAnomalies,
  getSourceHealth
} from '@/lib/api';

export const dynamic = 'force-dynamic';

export const metadata = {
  title: 'Admin Overview | MusePicker',
  description: 'Operational overview for source health, mapping review, and offer anomalies.',
  robots: {
    index: false,
    follow: false
  }
};

function EmptyState({ text }) {
  return <p className="muted">{text}</p>;
}

export default async function AdminPage() {
  let sourceHealth = [];
  let mappingQueue = [];
  let anomalies = [];

  try {
    [sourceHealth, mappingQueue, anomalies] = await Promise.all([
      getSourceHealth({ cache: 'no-store' }),
      getMappingReviewQueue({ cache: 'no-store' }),
      getOfferAnomalies({ cache: 'no-store' })
    ]);
  } catch {
    sourceHealth = [];
    mappingQueue = [];
    anomalies = [];
  }

  return (
    <section className="stack-lg">
      <section className="panel">
        <p className="eyebrow">Backoffice</p>
        <h1>Operational overview</h1>
        <p className="muted">
          This page is a read-only baseline for ingest and canonicalization monitoring. Add auth before production use.
        </p>
      </section>

      <section className="panel">
        <h2>Source Health</h2>
        {!sourceHealth.length ? (
          <EmptyState text="No source health records yet." />
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Source</th>
                  <th>Raw Offers</th>
                  <th>Mapped</th>
                  <th>Unmapped</th>
                </tr>
              </thead>
              <tbody>
                {sourceHealth.map((row) => (
                  <tr key={row.source}>
                    <td>{row.source}</td>
                    <td>{row.rawOfferCount}</td>
                    <td>{row.mappedCount}</td>
                    <td>{row.unmappedCount}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="panel">
        <h2>Mapping Review Queue</h2>
        {!mappingQueue.length ? (
          <EmptyState text="No mapping review items pending." />
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Source</th>
                  <th>Source Activity ID</th>
                  <th>Core Activity ID</th>
                  <th>MUALBA Activity ID</th>
                </tr>
              </thead>
              <tbody>
                {mappingQueue.map((row) => (
                  <tr key={`${row.source}-${row.sourceActivityId}`}>
                    <td>{row.source}</td>
                    <td>{row.sourceActivityId}</td>
                    <td>{row.coreActivityId || '-'}</td>
                    <td>{row.mualbaActivityId || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="panel">
        <h2>Offer Anomalies</h2>
        {!anomalies.length ? (
          <EmptyState text="No anomalous offers detected." />
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Offer ID</th>
                  <th>Reason</th>
                  <th>Effective Price</th>
                  <th>Availability</th>
                </tr>
              </thead>
              <tbody>
                {anomalies.map((row) => (
                  <tr key={row.offerId}>
                    <td>{row.offerId}</td>
                    <td>{row.reason}</td>
                    <td>{row.effectivePrice}</td>
                    <td>{row.availability}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </section>
  );
}
