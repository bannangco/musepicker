# Shimyunbo First Launch Runbook

This runbook launches MusePicker test production on:

- Web: `https://musepicker.shimyunbo.com`
- API: `https://api.musepicker.shimyunbo.com`

`shimyunbo.com` apex remains unchanged.

## 1. Cloudflare DNS Setup

In Cloudflare DNS for `shimyunbo.com`:

1. Add `CNAME` record:
   - Name: `musepicker`
   - Target: Vercel-provided CNAME target
   - Proxy status: DNS only during initial Vercel validation, then Proxied
2. Add `A` record:
   - Name: `api.musepicker`
   - Value: OCI VM public IPv4
   - Proxy status: DNS only while Caddy is first issuing TLS; Proxied after origin HTTPS works
3. SSL/TLS mode:
   - Start with `Full` if origin certificate is not ready
   - Switch to `Full (strict)` after Caddy issues a valid cert

## 2. Vercel Project Setup (`apps/web`)

1. Import GitHub repo: `bannangco/musepicker`
2. Set **Root Directory** to `apps/web`
3. Set environment variables (Production and Preview):
   - `NEXT_PUBLIC_SITE_URL=https://musepicker.shimyunbo.com`
   - `NEXT_PUBLIC_API_BASE_URL=https://api.musepicker.shimyunbo.com`
   - `API_BASE_URL=https://api.musepicker.shimyunbo.com`
4. Add custom domain: `musepicker.shimyunbo.com`
5. Confirm automatic deployments from your default branch (`master` in the current local repo, or `main` if you rename it later)

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
Keep `allowPublicKeyRetrieval=true` in `infra/env/api.prod.env` because MySQL 8.4 uses `caching_sha2_password` by default.

If the GitHub repository is private, configure host-side Git access first:

- preferred: add a read-only deploy key to the repo and use SSH clone URL
- alternative: set `OCI_REPO_URL` secret to a token-authenticated HTTPS URL

Manual first deploy:

```bash
bash infra/scripts/deploy_api_oci.sh
```

Verify:

```bash
curl -i https://api.musepicker.shimyunbo.com/api/healthz
```

## 5. GitHub Secrets for API Deploy Workflow

Add repository secrets:

- `OCI_HOST`: OCI VM public IP or hostname
- `OCI_USER`: SSH user (usually `ubuntu`)
- `OCI_SSH_PRIVATE_KEY`: private key for SSH auth
- `OCI_KNOWN_HOSTS`: output from `ssh-keyscan -H <host>` (recommended)
- `OCI_DEPLOY_PATH`: `/opt/musepicker` (optional, defaults provided)
- `OCI_REPO_URL`: `https://github.com/bannangco/musepicker.git` (optional)
- `OCI_DEPLOY_BRANCH`: default branch name, for example `master` or `main` (optional; omit to let the deploy script detect it)
- `OCI_API_HEALTH_URL`: `http://127.0.0.1:8080/api/healthz` (optional; omit to use this default)

Then ensure branch protection for your default branch requires `Monorepo CI` checks.

## 6. Deployment Automation Behavior

- Workflow: `.github/workflows/deploy-api.yml`
- Triggers on `main` or `master` when API/infra deploy files change
- Connects to OCI over SSH and runs `infra/scripts/deploy_api_oci.sh`
- Remote script:
  - syncs branch
  - rebuilds/restarts compose stack
  - checks local API health at `http://127.0.0.1:8080/api/healthz`
  - stores failure logs under `/opt/musepicker/.deploy-logs`

## 7. Multi-Service Routing on Oracle

Use one shared Caddy entry point for all services on the instance. MusePicker API owns `api.musepicker.shimyunbo.com` and proxies to the internal Docker service `api:8080`. Future services should get their own hostnames and Caddy blocks that proxy to their own internal container names and ports.

## 8. Smoke Test Checklist

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

## 9. Troubleshooting

If deploy fails with `fatal: couldn't find remote ref main`, the server is trying to deploy a branch that does not exist on GitHub. The deploy script now auto-detects the remote default branch when `DEPLOY_BRANCH` is not set. For GitHub Actions, set `OCI_DEPLOY_BRANCH` only if you intentionally want to pin a branch.

If API Docker build fails at `compileJava`, fix the Java compiler error first, push the change, then rerun `bash infra/scripts/deploy_api_oci.sh`.

If API logs show `Public Key Retrieval is not allowed`, update `infra/env/api.prod.env` so `DB_URL` includes `allowPublicKeyRetrieval=true`, then rerun deploy.

If deploy succeeds locally but public HTTPS fails with `sslv3 alert handshake failure`, separate API health from domain health:

```bash
curl -i http://127.0.0.1:8080/api/healthz
curl -i http://127.0.0.1:8080/api/regions/cities
docker logs musepicker-caddy --tail 100
```

If local API works, the remaining issue is DNS, Cloudflare proxy/TLS, Caddy certificate issuance, or domain registrar state.

If Cloudflare shows `The registrar services for this domain have been suspended by Cloudflare for a Terms of Service violation`, DNS changes will not fix the site. Resolve the domain suspension in Cloudflare Registrar/support first or temporarily use another working domain.
