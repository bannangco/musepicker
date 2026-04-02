# Launch Gates

## Product Gates

1. Public v1 endpoints pass contract + integration tests.
2. Search and ranking behavior is deterministic across reruns.
3. Affiliate outbound flow is verified end-to-end.
4. SEO/SSR checks pass for home/search/city/category/activity pages.

## Data Gates

1. Multi-source ingest adapters run stably with no schema contract violations.
2. Idempotency and dedup checks prevent duplicate canonical offers.
3. Canonical mapping queue is operational with manual override support.

## Security and Operations Gates

1. OIDC-only deployment auth and protected environment workflows.
2. Secret scanning and workflow policy checks pass.
3. Monitoring and alert routing are enabled for API + ingest failures.
