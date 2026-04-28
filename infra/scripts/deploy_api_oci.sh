#!/usr/bin/env bash
set -euo pipefail

DEPLOY_ROOT="${DEPLOY_ROOT:-/opt/musepicker}"
REPO_URL="${REPO_URL:-https://github.com/bannangco/musepicker.git}"
DEPLOY_BRANCH="${DEPLOY_BRANCH:-}"
COMPOSE_FILE="${COMPOSE_FILE:-infra/docker-compose.prod.yml}"
API_HEALTH_URL="${API_HEALTH_URL:-https://api.musepicker.shimyunbo.com/api/healthz}"
HEALTH_RETRIES="${HEALTH_RETRIES:-30}"
HEALTH_SLEEP_SECONDS="${HEALTH_SLEEP_SECONDS:-2}"
DEPLOY_LOG_DIR="${DEPLOY_LOG_DIR:-${DEPLOY_ROOT}/.deploy-logs}"

ENV_FILES=(
  "infra/env/db.prod.env"
  "infra/env/api.prod.env"
  "infra/env/caddy.prod.env"
)

require_binary() {
  local binary="$1"
  if ! command -v "$binary" >/dev/null 2>&1; then
    echo "Missing required binary: $binary"
    exit 1
  fi
}

require_binary git
require_binary docker
require_binary curl

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 plugin is required (docker compose)."
  exit 1
fi

mkdir -p "$DEPLOY_ROOT"
mkdir -p "$DEPLOY_LOG_DIR"

if [ ! -d "$DEPLOY_ROOT/.git" ]; then
  echo "[deploy] cloning repository into $DEPLOY_ROOT"
  git clone "$REPO_URL" "$DEPLOY_ROOT"
fi

cd "$DEPLOY_ROOT"

if [ -z "$DEPLOY_BRANCH" ]; then
  DEPLOY_BRANCH="$(git ls-remote --symref origin HEAD 2>/dev/null | awk '/^ref:/ { sub("refs/heads/", "", $2); print $2; exit }')"
fi

if [ -z "$DEPLOY_BRANCH" ]; then
  if git ls-remote --exit-code --heads origin main >/dev/null 2>&1; then
    DEPLOY_BRANCH="main"
  elif git ls-remote --exit-code --heads origin master >/dev/null 2>&1; then
    DEPLOY_BRANCH="master"
  else
    echo "Could not determine deploy branch. Set DEPLOY_BRANCH or OCI_DEPLOY_BRANCH."
    exit 1
  fi
fi

echo "[deploy] syncing branch $DEPLOY_BRANCH"
git fetch origin "$DEPLOY_BRANCH"
git checkout "$DEPLOY_BRANCH"
git pull --ff-only origin "$DEPLOY_BRANCH"

for env_file in "${ENV_FILES[@]}"; do
  if [ ! -f "$env_file" ]; then
    echo "Missing required env file: $env_file"
    echo "Copy the matching .example file from infra/env before deploying."
    exit 1
  fi
done

compose_cmd=(docker compose)
for env_file in "${ENV_FILES[@]}"; do
  compose_cmd+=(--env-file "$env_file")
done
compose_cmd+=(-f "$COMPOSE_FILE")

echo "[deploy] building and starting production stack"
"${compose_cmd[@]}" up -d --build --remove-orphans

echo "[deploy] waiting for API health endpoint: $API_HEALTH_URL"
health_ok=0
for ((attempt = 1; attempt <= HEALTH_RETRIES; attempt++)); do
  if curl -fsS "$API_HEALTH_URL" >/dev/null; then
    health_ok=1
    echo "[deploy] health check passed on attempt $attempt"
    break
  fi
  sleep "$HEALTH_SLEEP_SECONDS"
done

if [ "$health_ok" -ne 1 ]; then
  timestamp="$(date -u +"%Y%m%dT%H%M%SZ")"
  fail_log="$DEPLOY_LOG_DIR/deploy-failure-$timestamp.log"
  echo "[deploy] health check failed; collecting container logs -> $fail_log"
  "${compose_cmd[@]}" ps || true
  "${compose_cmd[@]}" logs --no-color --timestamps > "$fail_log" || true
  exit 1
fi

echo "[deploy] stack status"
"${compose_cmd[@]}" ps

echo "[deploy] completed successfully"
