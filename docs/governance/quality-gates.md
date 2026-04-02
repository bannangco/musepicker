# Quality Gates

These gates are required for promotion.

## Mandatory

1. OpenAPI validation (`packages/contracts/openapi/musepicker-v1.yaml`).
2. JSON schema validation (`packages/contracts/scripts/validate_schemas.py`).
3. API automated test suite pass.
4. Ingest adapter contract/idempotency/quality tests pass.
5. Web production build pass.
6. Flyway migration naming and schema checks pass.
7. Security workflow checks pass (`scripts/check_workflow_policy.sh`).

## Functional

1. Ranking determinism tests pass.
2. Search filter regression tests pass.
3. Affiliate outbound attribution behavior is verified.
4. SSR/SEO checks pass for core pages.

## Operational

1. Structured logs include correlation/request IDs.
2. Ingest run logs and source metrics are generated.
3. Alerting/runbook docs are updated for new failure modes.
