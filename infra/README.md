# Infra Blueprint

This directory holds runtime/deployment artifacts for MusePicker first launch on `shimyunbo.com` test hosts.

## Runtime Topology (Current)

- **Cloudflare Free**
  - DNS + edge proxy for `musepicker.shimyunbo.com` (Vercel) and `api.shimyunbo.com` (OCI origin)
- **Vercel Hobby**
  - Hosts `apps/web`
- **OCI Always Free VM**
  - Runs `infra/docker-compose.prod.yml`
  - Services: `mysql`, `api`, `caddy`
- **GitHub Actions**
  - CI gate (`.github/workflows/ci.yml`)
  - API deploy over SSH (`.github/workflows/deploy-api.yml`)

## Key Files

- `docker-compose.dev.yml`: local dev stack
- `docker-compose.prod.yml`: OCI production stack for API + DB + Caddy
- `Caddyfile`: HTTPS reverse proxy for `api.shimyunbo.com`
- `env/*.example`: production env templates
- `scripts/deploy_api_oci.sh`: remote deploy script used by GitHub Actions
- `scripts/bootstrap_oci_host.sh`: host bootstrap helper script for Ubuntu OCI VMs

## Security Requirements

- No static secrets in repository.
- Store deploy credentials in GitHub secrets.
- Limit OCI ingress to only `22`, `80`, `443`.
- Keep `main` branch protected and CI-required.
