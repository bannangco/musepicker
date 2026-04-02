# MusePicker Contracts

This package stores public API contracts and shared schemas.

- `openapi/musepicker-v1.yaml`: stable REST API contract
- `schemas/*.schema.json`: shared JSON schemas for data exchange

## Rules

1. Contracts-first: update this package before behavior changes in `apps/api` or `apps/ingest`.
2. v1 endpoints are backward compatible by default.
3. Shared ingest payloads (`RawOffer`) are mandatory for source adapters.

## Validation

```bash
python -m openapi_spec_validator packages/contracts/openapi/musepicker-v1.yaml
python packages/contracts/scripts/validate_schemas.py
```
