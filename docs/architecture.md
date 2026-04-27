# MusePicker Rebuild Architecture (Implemented Baseline)

## Reuse Decision

| Repository | Decision | Notes |
| --- | --- | --- |
| `musepicker_back` | Reuse concepts, rewrite production code | Security incident removed, old config scrubbed, new API implemented in `apps/api`. |
| `musepicker_front` | Do not reuse code | Old React prototype is mock-level only. |
| `musepicker_front_nextjs` | Bootstrap reference only | Replaced with new `apps/web` implementation. |
| `musepicker_scraper` | Reuse data/selector patterns | New adapters and fixture-driven tests in `apps/ingest`. |

Active development repository:

- `bannangco/musepicker`
- https://github.com/bannangco/musepicker

## Monorepo Shape

- `apps/web`: Next.js App Router frontend
- `apps/api`: Spring Boot 3.x API
- `apps/ingest`: Python ingestion workers
- `packages/contracts`: OpenAPI + JSON schemas
- `infra`: container + IaC + runtime blueprint

## Data Model Strategy

Single DB now, split-ready later:

- `core_*`: private MusePicker operational model
- `mualba_*`: canonical exportable/public standard model
- `source_*`: raw ingestion snapshots and source-to-canonical mapping

## API v1

- `GET /api/healthz` (deployment/uptime health)
- `GET /api/regions/cities`
- `GET /api/activities/trending`
- `GET /api/activities/search`
- `GET /api/activities/{activityId}`
- `GET /api/activities/{activityId}/offers`
- `GET /api/platforms`
- `GET /api/affiliate/out/{offerId}` (click tracking + redirect)
- `GET /api/mualba/activities` (canonical export surface)
- `GET /api/admin/sources/health` (backoffice health)
- `GET /api/admin/mappings/review` (backoffice review queue)
- `POST /api/admin/mappings/override` (manual mapping hook)
- `GET /api/admin/offers/anomalies` (backoffice anomaly queue)

Compatibility aliases are retained for legacy consumers:

- `POST /api/activities/search`
- `GET /api/activities/{activityId}/tickets`

## Ingestion Flow

1. Source adapter fetches raw data (API-first).
2. Offers normalized to shared `RawOffer`.
3. Quality checks + dedup validation.
4. Idempotency key check avoids duplicates.
5. Snapshot append for trend/anomaly history.
6. Canonical mapping confidence generated; low-confidence items land in review queue.
7. Dead-letter entries capture quality and adapter failures for replay.
8. Run logs + per-source health metrics updated.

## Security Phase 0 Status

- Removed exfiltration workflow from legacy backend.
- Removed hardcoded DB/API secrets from legacy `application.properties`.
- Added incident-response checklist in `SECURITY_INCIDENT_RESPONSE.md`.

## First Launch Runtime (Test Domain)

- Web: `https://musepicker.shimyunbo.com` on Vercel
- API: `https://api.musepicker.shimyunbo.com` on OCI VM (`mysql` + `api` + `caddy`)
- DNS/edge: Cloudflare Free
