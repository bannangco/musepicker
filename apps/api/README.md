# MusePicker API

Spring Boot 3.x API for MusePicker public v1 endpoints.

## Key Points

- Java 21
- Flyway migrations for schema lifecycle
- Split-ready table boundaries:
  - `core_*` for private MusePicker operations
  - `mualba_*` for canonical/public-standard entities
  - `source_*` for raw ingest payloads and mapping
- Compatibility aliases maintained for legacy frontend behavior.

## Run

```bash
cd apps/api
./gradlew bootRun
```

## Test

```bash
cd apps/api
./gradlew test
```

## API Endpoints (v1)

- `GET /api/regions/cities`
- `GET /api/activities/trending`
- `GET /api/activities/search`
- `GET /api/activities/{activityId}`
- `GET /api/activities/{activityId}/offers`
- `GET /api/platforms`
