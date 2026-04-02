from datetime import datetime, timezone
from decimal import Decimal

from musepicker_ingest.adapters.base import SourceAdapter
from musepicker_ingest.config import IngestConfig
from musepicker_ingest.models import AdapterResult, RawOffer
from musepicker_ingest.pipeline.runner import IngestRunner


class StaticAdapter(SourceAdapter):
    source_name = "static_source"

    def __init__(self, offers):
        super().__init__(fixture_path=None)
        self._offers = offers

    def fetch_raw_offers(self, since=None):
        return AdapterResult(source=self.source_name, offers=self._offers, fetched_at=datetime.now(timezone.utc))


def test_idempotency_prevents_duplicate_snapshots(tmp_path):
    offer = RawOffer(
        source="static_source",
        source_offer_id="offer-1",
        source_activity_id="activity-1",
        title="Test Offer",
        city="Seoul",
        category="Museums & Galleries",
        currency="USD",
        base_price=Decimal("25.00"),
        affiliate_url="https://example.com/book/1",
    )
    adapter = StaticAdapter([offer, offer])
    runner = IngestRunner(config=IngestConfig(root_dir=tmp_path), adapters=[adapter])

    first = runner.run(source="static_source", dry_run=False)
    second = runner.run(source="static_source", dry_run=False)

    first_stats = first["sources"][0]
    second_stats = second["sources"][0]

    assert first_stats["accepted"] == 1
    assert first_stats["duplicates"] == 0
    assert second_stats["accepted"] == 0
    assert second_stats["duplicates"] == 1
