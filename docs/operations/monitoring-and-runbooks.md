# Monitoring and Runbooks

## Core Signals

1. API availability and latency for `/api/activities/search`, `/api/activities/{id}/offers`.
2. Ingest success/failure ratio by source.
3. Dead-letter volume by source and reason.
4. Affiliate outbound click throughput and error rate.

## Correlation

1. API requests carry `X-Request-Id`.
2. Logs include request/run correlation IDs.
3. Ingest run summary includes per-source stats and failure details.

## Runbooks

1. Ingest source outage:
   - Confirm adapter health metrics
   - Inspect latest run log and dead-letter records
   - Trigger replay for impacted source payloads
2. Ranking anomaly:
   - Validate effective price formula and tie-break ordering
   - Check currency normalization and offer availability fields
3. Affiliate redirect issue:
   - Verify outbound endpoint response and destination
   - Verify click event persistence and partner parameters
