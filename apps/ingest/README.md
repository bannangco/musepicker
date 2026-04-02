# MusePicker Ingest

`apps/ingest` contains production ingestion workers for MusePicker.

## Design

- API-first adapters: Klook, Trip.com, TicketsToDo, Viator
- Scraper fallback adapter when official API access is unavailable
- Shared normalized payload: `RawOffer`
- Built-in retries with exponential backoff
- Idempotency keys to prevent duplicate canonical ingest
- Run logs + per-source health metrics
- Dead-letter store for adapter/quality failures
- Replay mode for dead-letter recovery
- Canonical mapping store with confidence score + review queue
- Offer snapshot storage for trend and anomaly analysis

## Run

```bash
cd apps/ingest
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m musepicker_ingest.pipeline.run_ingest --source klook --fixture tests/fixtures/klook_museum_list.sample.json
```

## Replay Dead Letters

```bash
python -m musepicker_ingest.pipeline.run_ingest --replay-dead-letters --source klook
```

## Show Mapping Review Queue

```bash
python -m musepicker_ingest.pipeline.run_ingest --source klook --fixture tests/fixtures/klook_museum_list.sample.json --show-review-queue
```

## Test

```bash
pytest
```
