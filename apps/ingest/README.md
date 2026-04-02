# MusePicker Ingest

`apps/ingest` contains production ingestion workers for MusePicker.

## Design

- API-first adapters: Klook, Trip.com, TicketsToDo, Viator
- Scraper fallback adapter when official API access is unavailable
- Shared normalized payload: `RawOffer`
- Built-in retries with exponential backoff
- Idempotency keys to prevent duplicate canonical ingest
- Run logs + per-source health metrics
- Offer snapshot storage for trend and anomaly analysis

## Run

```bash
cd apps/ingest
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m musepicker_ingest.pipeline.run_ingest --source klook --fixture tests/fixtures/klook_museum_list.sample.json
```

## Test

```bash
pytest
```
