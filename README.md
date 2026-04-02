# MusePicker Monorepo

MusePicker is a metasearch platform for cultural activity tickets (museums, galleries, theatre, attractions) with price comparison and affiliate outbound routing.

## Repository Layout

- `apps/web`: Next.js frontend (App Router, React Query, URL-driven filters)
- `apps/api`: Spring Boot API (v1 public contract, MUALBA split-ready schema)
- `apps/ingest`: Python ingestion workers (API-first adapters + scraper fallback)
- `packages/contracts`: OpenAPI + JSON Schemas
- `infra`: Infrastructure and CI/CD scaffolding

## Implemented Rebuild Baseline

- Monorepo structure created and wired (`web`, `api`, `ingest`, `contracts`, `infra`).
- API v1 contract added in `packages/contracts/openapi/musepicker-v1.yaml`.
- Spring API scaffolded with split-ready DB boundaries:
  - `core_*`: private operational entities
  - `mualba_*`: canonical standard entities
  - `source_*`: raw ingestion payloads and mapping
- Next.js web scaffolded with:
  - URL-driven filters
  - React Query server-state
  - Search/detail pages
  - Affiliate outbound redirect tracking route
- Ingestion workers scaffolded with:
  - API-first adapters (`klook`, `tripcom`, `ticketstodo`, `viator`)
  - scraper fallback adapter
  - retries/backoff, idempotency, snapshot persistence, health metrics
  - dead-letter store, replay flow, canonical mapping confidence/review queue
  - contract/idempotency/data-quality test suite
- Root CI workflows added:
  - security checks
  - OpenAPI contract validation
  - JSON schema validation
  - API/web/ingest build-test gates
  - migration naming gate

## Legacy Repositories

The historical prototype repositories are legacy-only.

Those legacy repos are:

- `musepicker_back`
- `musepicker_front`
- `musepicker_front_nextjs`
- `musepicker_scraper`

Active development moved to:

- `bannangco/musepicker`
- https://github.com/bannangco/musepicker

Do not treat the legacy repos as production-ready services.

## Quick Start

### API

```bash
cd apps/api
./gradlew bootRun
```

### Web

```bash
cd apps/web
npm install
npm run dev
```

### Ingest

```bash
cd apps/ingest
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m musepicker_ingest.pipeline.run_ingest --source klook --fixture tests/fixtures/klook_museum_list.sample.json --dry-run
```

## Security Baseline

- No secrets should be committed in source control.
- Use environment variables or secret manager integration for runtime config.
- GitHub Actions must use OIDC and protected environments.
- See `SECURITY_INCIDENT_RESPONSE.md` for the removed legacy exfiltration workflow response checklist.

## Additional Docs

- `docs/architecture.md`: rebuild architecture and reuse decisions
- `docs/governance/`: policies, ADR, quality gates
- `docs/operations/`: monitoring, launch gates, post-launch loop
