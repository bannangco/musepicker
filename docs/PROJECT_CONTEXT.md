# PROJECT_CONTEXT.md

This is the required first-read file for any new Codex/ChatGPT session working on `bannangco/musepicker`.

## 1. Project State Snapshot

MusePicker is a metasearch platform for museum/gallery/theater/activity tickets.

Current launch phase:

- Public test domain: `musepicker.shimyunbo.com`
- Public API domain: `api.musepicker.shimyunbo.com`
- Data source mode: seeded dummy data only (Flyway migrations)
- Ingestion adapters/pipeline are scaffolded but not used for live data yet

## 2. Monorepo Structure and Roles

- `apps/web`: Next.js App Router customer web app
- `apps/api`: Spring Boot API (v1 contract + affiliate redirect + admin/backoffice endpoints)
- `apps/ingest`: Python ingestion runtime and tests (phase-2 activation)
- `packages/contracts`: OpenAPI and JSON Schemas
- `infra`: deployment/runtime artifacts (compose, Caddy, env templates, scripts)
- `docs`: architecture/governance/operations documentation

## 3. Current Customer Web Behavior

### Route Map

- `/` global home (city-first + trending + petition CTA)
- `/city/[city]` region home (hero, categories, promo rail, paged popular tickets)
- `/search` list UI with filters/sort
- `/category/[category]` category list UI
- `/activity/[activityId]` detail page with grouped offers + placeholders (map/nearby/reviews)
- `/out/[offerId]` compatibility redirect route -> API affiliate out endpoint
- `/admin` backoffice page exists but hidden from public nav and disallowed in robots

### SEO/robots

- Default site URL base: `https://musepicker.shimyunbo.com`
- `robots.txt` disallows `/admin`
- sitemap generated from cities + trending data

## 4. API Surface (Current)

### Public/Search

- `GET /api/regions/cities`
- `GET /api/activities/trending`
- `GET /api/activities/search`
- `GET /api/activities/{activityId}`
- `GET /api/activities/{activityId}/offers`
- `GET /api/platforms`

### Affiliate

- `GET /api/affiliate/out/{offerId}`
  - validates target URL
  - writes `core_affiliate_click`
  - appends platform-specific tracking params
  - returns 302 redirect

### Operational

- `GET /api/healthz` (used by deploy checks/uptime)

### Backoffice/Internal

- `GET /api/mualba/activities`
- `GET /api/admin/sources/health`
- `GET /api/admin/mappings/review`
- `POST /api/admin/mappings/override`
- `GET /api/admin/offers/anomalies`

## 5. Data and Seed Model

Database boundaries are split-ready in one DB:

- `core_*`: private operations (activities/offers/platforms/schedules/affiliate clicks)
- `source_*`: raw ingest payloads/mappings/dead letters/replay events
- `mualba_*`: canonical exportable standard entities

Seed notes:

- Initial seed in `V1__init.sql`
- `V2__hardening_affiliate_and_admin.sql` adds click and admin-related tables/indexes
- `V3__refresh_demo_seed_dates.sql` keeps demo schedules in future dates for stable UI demos

## 6. Deployment Topology and Automation

### Hosting

- Web: Vercel Hobby (`apps/web` root)
- API+DB: OCI VM running Docker Compose production stack
- Edge/DNS: Cloudflare Free

### OCI stack

- Compose file: `infra/docker-compose.prod.yml`
- Services: `db` (MySQL), `api` (Spring Boot), `caddy` (TLS reverse proxy)
- Proxy config: `infra/Caddyfile`
- Env templates: `infra/env/*.example`
- Multi-service rule: Caddy owns public `80/443`; every service gets its own hostname block and internal Docker target.

### CI/CD

- CI: `.github/workflows/ci.yml`
- API deploy: `.github/workflows/deploy-api.yml`
  - trigger: push to `main` (API/infra deploy paths) + manual dispatch
  - action: SSH to OCI VM and run `infra/scripts/deploy_api_oci.sh`
  - health gate: checks `https://api.musepicker.shimyunbo.com/api/healthz`
  - failure logs stored on host under `/opt/musepicker/.deploy-logs`

## 7. Environment Variable Matrix

### `apps/web` (Vercel)

- `NEXT_PUBLIC_SITE_URL=https://musepicker.shimyunbo.com`
- `NEXT_PUBLIC_API_BASE_URL=https://api.musepicker.shimyunbo.com`
- `API_BASE_URL=https://api.musepicker.shimyunbo.com`

### `apps/api` runtime

- `PORT=8080`
- `DB_URL=jdbc:mysql://db:3306/musepicker?useSSL=false&serverTimezone=UTC`
- `DB_USERNAME=musepicker`
- `DB_PASSWORD=<secret>`
- `DB_DRIVER=com.mysql.cj.jdbc.Driver`
- `CORS_ALLOWED_ORIGINS=https://musepicker.shimyunbo.com`

### GitHub secrets (deploy workflow)

- `OCI_HOST`
- `OCI_USER`
- `OCI_SSH_PRIVATE_KEY`
- `OCI_KNOWN_HOSTS`
- `OCI_DEPLOY_PATH` (optional)
- `OCI_REPO_URL` (optional)
- `OCI_DEPLOY_BRANCH` (optional)
- `OCI_API_HEALTH_URL` (optional)

## 8. Known Gaps / Next Milestone

- No live partner API integrations yet (Klook/Viator/Trip.com/TicketsToDo not connected in production)
- Nearby/review/map are UI placeholders pending backend domains/data
- Backoffice auth and RBAC are not production-hardened yet
- Terraform directory is placeholder and not driving production infra

## 9. Last Rollout Change Set (Shimyunbo Test Launch)

- Replaced AWS placeholder deploy workflow with OCI SSH deploy workflow
- Added OCI production compose stack + Caddy reverse proxy config
- Added production env templates under `infra/env`
- Added remote deploy script and OCI bootstrap helper script
- Added API health endpoint `/api/healthz`
- Added Flyway migration to refresh demo schedule dates
- Updated web default domain examples for `musepicker.shimyunbo.com`
- Added first-launch runbook for Cloudflare/Vercel/OCI/GitHub setup

## 10. Handoff Rules for New Sessions

1. Read this file first.
2. Read `docs/operations/SHIMYUNBO_FIRST_LAUNCH.md` before touching deployment.
3. Do not run destructive git commands on server/repo without explicit user instruction.
4. Keep public API contract stable unless migration plan is explicitly approved.
5. Prefer adding migrations over editing old migration files.
