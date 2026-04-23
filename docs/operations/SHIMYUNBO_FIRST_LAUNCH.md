# Shimyunbo First Launch Runbook

This runbook launches MusePicker test production on:

- Web: `https://musepicker.shimyunbo.com`
- API: `https://api.shimyunbo.com`

`shimyunbo.com` apex remains unchanged.

## 1. Cloudflare DNS Setup

In Cloudflare DNS for `shimyunbo.com`:

1. Add `CNAME` record:
   - Name: `musepicker`
   - Target: Vercel-provided CNAME target
   - Proxy status: DNS only during initial Vercel validation, then Proxied
2. Add `A` record:
   - Name: `api`
   - Value: OCI VM public IPv4
   - Proxy status: Proxied
3. SSL/TLS mode:
   - Start with `Full` if origin certificate is not ready
   - Switch to `Full (strict)` after Caddy issues a valid cert

## 2. Vercel Project Setup (`apps/web`)

1. Import GitHub repo: `bannangco/musepicker`
2. Set **Root Directory** to `apps/web`
3. Set environment variables (Production and Preview):
   - `NEXT_PUBLIC_SITE_URL=https://musepicker.shimyunbo.com`
   - `NEXT_PUBLIC_API_BASE_URL=https://api.shimyunbo.com`
   - `API_BASE_URL=https://api.shimyunbo.com`
4. Add custom domain: `musepicker.shimyunbo.com`
5. Confirm automatic deployments from `main`

## 3. OCI VM Provisioning (Always Free)

1. Create Ubuntu VM in OCI Always Free
2. Open ingress ports in OCI security list / NSG:
   - `22/tcp` (SSH)
   - `80/tcp` (HTTP)
   - `443/tcp` (HTTPS)
3. SSH into VM and bootstrap:

```bash
# on OCI host
cd /tmp
git clone https://github.com/bannangco/musepicker.git
cd musepicker
bash infra/scripts/bootstrap_oci_host.sh
```

4. Re-login so docker group membership applies.

## 4. OCI Host App Runtime Preparation

```bash
sudo mkdir -p /opt/musepicker
sudo chown -R "$USER":"$USER" /opt/musepicker
cd /opt/musepicker
git clone https://github.com/bannangco/musepicker.git .
mkdir -p infra/env
cp infra/env/db.prod.env.example infra/env/db.prod.env
cp infra/env/api.prod.env.example infra/env/api.prod.env
cp infra/env/caddy.prod.env.example infra/env/caddy.prod.env
```

Edit the copied `infra/env/*.env` files with real secrets.

If the GitHub repository is private, configure host-side Git access first:

- preferred: add a read-only deploy key to the repo and use SSH clone URL
- alternative: set `OCI_REPO_URL` secret to a token-authenticated HTTPS URL

Manual first deploy:

```bash
bash infra/scripts/deploy_api_oci.sh
```

Verify:

```bash
curl -i https://api.shimyunbo.com/api/healthz
```

## 5. GitHub Secrets for API Deploy Workflow

Add repository secrets:

- `OCI_HOST`: OCI VM public IP or hostname
- `OCI_USER`: SSH user (usually `ubuntu`)
- `OCI_SSH_PRIVATE_KEY`: private key for SSH auth
- `OCI_KNOWN_HOSTS`: output from `ssh-keyscan -H <host>` (recommended)
- `OCI_DEPLOY_PATH`: `/opt/musepicker` (optional, defaults provided)
- `OCI_REPO_URL`: `https://github.com/bannangco/musepicker.git` (optional)
- `OCI_DEPLOY_BRANCH`: `main` (optional)
- `OCI_API_HEALTH_URL`: `https://api.shimyunbo.com/api/healthz` (optional)

Then ensure branch protection for `main` requires `Monorepo CI` checks.

## 6. Deployment Automation Behavior

- Workflow: `.github/workflows/deploy-api.yml`
- Triggers on `main` when API/infra deploy files change
- Connects to OCI over SSH and runs `infra/scripts/deploy_api_oci.sh`
- Remote script:
  - syncs branch
  - rebuilds/restarts compose stack
  - checks `/api/healthz`
  - stores failure logs under `/opt/musepicker/.deploy-logs`

## 7. Smoke Test Checklist

1. Web pages render:
   - `/`
   - `/city/New%20York`
   - `/search`
   - `/category/museums%20%26%20galleries`
   - `/activity/<existing-seeded-uuid>`
2. API endpoints return data:
   - `/api/regions/cities`
   - `/api/activities/trending`
   - `/api/activities/search?city=New%20York`
   - `/api/platforms`
   - `/api/healthz`
3. Affiliate flow:
   - Click `View deal` on activity detail
   - Confirm redirect is 302 and destination includes MusePicker tracking params
4. SEO baseline:
   - `/robots.txt` disallows `/admin`
   - `/sitemap.xml` lists test-domain URLs
