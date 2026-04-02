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


def test_invalid_offer_is_written_to_dead_letter(tmp_path):
    invalid_offer = RawOffer(
        source="static_source",
        source_offer_id="offer-1",
        source_activity_id="activity-1",
        title="Invalid Offer",
        city="Seoul",
        category="Museums",
        currency="USD",
        base_price=Decimal("19.00"),
        affiliate_url="",
    )
    adapter = StaticAdapter([invalid_offer])
    runner = IngestRunner(config=IngestConfig(root_dir=tmp_path), adapters=[adapter])

    summary = runner.run(source="static_source", dry_run=False)
    stats = summary["sources"][0]

    assert stats["invalid"] == 1
    assert stats["dead_letters"] == 1
    assert stats["accepted"] == 0
    assert len(runner.dead_letters.list_unreplayed(source="static_source")) == 1


def test_replay_dead_letter_accepts_valid_offer(tmp_path):
    runner = IngestRunner(config=IngestConfig(root_dir=tmp_path), adapters=[])
    payload_offer = RawOffer(
        source="static_source",
        source_offer_id="offer-replay-1",
        source_activity_id="activity-replay-1",
        title="Replay Offer",
        city="New York",
        category="Museums",
        currency="USD",
        base_price=Decimal("29.00"),
        affiliate_url="https://example.com/replay",
    )
    runner.dead_letters.add(
        source="static_source",
        run_id="seed-run",
        reason="manual_test",
        payload=payload_offer.to_dict(),
    )

    summary = runner.replay_dead_letters(source="static_source", dry_run=False)
    stats = summary["sources"][0]

    assert stats["accepted"] == 1
    assert stats["duplicates"] == 0
    assert len(runner.dead_letters.list_unreplayed(source="static_source")) == 0
