# Infra Blueprint

This directory holds infrastructure and deployment scaffolding for the rebuilt MusePicker monorepo.

## Runtime Topology

- **Cloudflare** in front of `web` and `api` (DNS, CDN, WAF, TLS termination).
- **AWS** backend runtime:
  - `apps/web`: containerized Next.js service (or static+edge mode based on final deployment choice).
  - `apps/api`: containerized Spring Boot service.
  - `apps/ingest`: scheduled container jobs (EventBridge + ECS/Fargate or equivalent).
  - Managed MySQL (`core_*`, `mualba_*`, `source_*` schemas/tables).

## Files

- `docker-compose.dev.yml`: local compose stack (api + db + web + ingest runner).
- `terraform/`: IaC scaffold for AWS + Cloudflare integration points.

## Security Requirements

- No static cloud credentials in repo.
- GitHub Actions deploy workflows must use OIDC role assumption.
- Protected environments required for `staging` and `production`.
