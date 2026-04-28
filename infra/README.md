# Infra Blueprint

This directory holds runtime/deployment artifacts for MusePicker first launch on `shimyunbo.com` test hosts.

## Runtime Topology (Current)

- **Cloudflare Free**
  - DNS + edge proxy for `musepicker.shimyunbo.com` (Vercel) and `api.musepicker.shimyunbo.com` (OCI origin)
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
- `Caddyfile`: HTTPS reverse proxy for `api.musepicker.shimyunbo.com`
- `env/*.example`: production env templates
- `scripts/deploy_api_oci.sh`: remote deploy script used by GitHub Actions
- `scripts/bootstrap_oci_host.sh`: host bootstrap helper script for Ubuntu OCI VMs

## Multi-Service Routing on OCI

Caddy is the shared public entry point for the Oracle instance. Keep ports `80` and `443` owned by Caddy, then add each future service as a separate hostname block in `Caddyfile` that proxies to its internal Docker service and port. Do not expose individual app containers directly to the public internet.

## Security Requirements

- No static secrets in repository.
- Store deploy credentials in GitHub secrets.
- Limit OCI ingress to only `22`, `80`, `443`.
- Keep the default branch protected and CI-required.
