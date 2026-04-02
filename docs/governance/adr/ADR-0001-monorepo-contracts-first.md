# ADR-0001: Monorepo and Contracts-First Architecture

## Status

Accepted

## Context

MusePicker requires tightly coordinated evolution across web, API, ingest, contracts, and infra. Legacy multi-repo prototypes caused drift in interface assumptions and delivery quality.

## Decision

1. Use one active monorepo: `bannangco/musepicker`.
2. Make `packages/contracts` the source of truth for public interfaces.
3. Keep service boundaries:
   - `apps/web`
   - `apps/api`
   - `apps/ingest`
4. Keep one operational DB with split-ready ownership boundaries:
   - `core_*`
   - `source_*`
   - `mualba_*`

## Consequences

1. Cross-service changes become atomic and reviewable in one PR.
2. Contract drift risk is reduced.
3. CI must validate contract + behavior together.
4. Legacy repositories are reference-only and non-authoritative.
