# Coding Standards

## Baseline

1. Contracts-first changes: update `packages/contracts` before implementing behavior.
2. Backward compatibility by default for published endpoints.
3. No secrets in source control.
4. Prefer deterministic logic over heuristic ordering in ranking/comparison paths.
5. Every behavior change must include tests or explicit test-gap note.

## API (`apps/api`)

1. Controller DTOs must be versioned under `dto/v1`.
2. Validation happens at API boundary (`@Valid`, constraints, explicit request checks).
3. Exceptions must return standard error envelope.
4. DB schema changes must go through Flyway migrations only.

## Web (`apps/web`)

1. URL-driven filter state is source of truth for search pages.
2. Affiliate outbound actions must include click attribution path.
3. SSR pages must fail gracefully when upstream API is unavailable.

## Ingest (`apps/ingest`)

1. Adapters must emit normalized `RawOffer`.
2. Idempotency key is required before persistence.
3. Invalid records must be captured in dead-letter logs.
4. Adapter changes require fixture-based contract tests.
