# API Versioning Policy

## Public API Surface

The stable public surface is the v1 contract in `packages/contracts/openapi/musepicker-v1.yaml`.

## Rules

1. No breaking change on existing v1 fields, response envelopes, or endpoint meanings.
2. New fields must be additive and optional unless endpoint is introduced as new.
3. Breaking changes require a new versioned path namespace (for example `/api/v2/...`).
4. Compatibility aliases may be maintained during migrations but must be explicitly documented.
5. Error envelope shape is stable across endpoints.

## Contract Change Workflow

1. Update OpenAPI + JSON schema first.
2. Add/adjust contract tests.
3. Implement service behavior changes.
4. Verify generated/consumer integrations.
