#!/usr/bin/env bash
set -euo pipefail

WORKFLOW_DIR=".github/workflows"

if [ ! -d "$WORKFLOW_DIR" ]; then
  echo "No workflow directory found: $WORKFLOW_DIR"
  exit 1
fi

# Block known secret-exfiltration patterns.
if grep -RInE "curl.+\$\{\{\s*secrets\." "$WORKFLOW_DIR"; then
  echo "Detected suspicious workflow command pattern."
  exit 1
fi

# Block direct external curl/wget downloads from workflow scripts.
if grep -RInE "(curl|wget)[[:space:]].*https?://" "$WORKFLOW_DIR"; then
  echo "Direct curl/wget network calls are not allowed in workflows."
  exit 1
fi

# Enforce OIDC for deploy workflows.
for workflow in "$WORKFLOW_DIR"/*deploy*.yml "$WORKFLOW_DIR"/*deploy*.yaml; do
  if [ ! -f "$workflow" ]; then
    continue
  fi
  if ! grep -Eq "id-token:\s*write" "$workflow"; then
    echo "Deploy workflow missing 'id-token: write' permission: $workflow"
    exit 1
  fi
done

echo "Workflow policy checks passed."
