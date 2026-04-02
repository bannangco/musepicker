# Migration Policy

## Flyway Naming

1. Every schema change is a new immutable Flyway file: `V{N}__{description}.sql`.
2. Existing migration files must never be edited after shared use.
3. Data correction after release must be additive via new migration.

## Data Safety Rules

1. Add constraints and indexes incrementally with compatibility in mind.
2. Destructive operations require explicit rollback and data-recovery note.
3. New tables must define ownership (`core_*`, `source_*`, `mualba_*`).
4. Seed data in migrations should be minimal and deterministic.

## Review Requirements

1. Migration reviewed by API/data owner.
2. Migration gate CI must pass.
3. Integration behavior verified against migrated schema.
