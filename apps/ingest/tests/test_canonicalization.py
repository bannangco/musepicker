from decimal import Decimal

from musepicker_ingest.models import RawOffer
from musepicker_ingest.pipeline.canonicalization import CanonicalMappingStore


def test_canonicalization_review_queue_and_override(tmp_path):
    store = CanonicalMappingStore(tmp_path / "canonicalization.sqlite3", review_threshold=0.8)
    offer = RawOffer(
        source="klook",
        source_offer_id="offer-1",
        source_activity_id="activity-1",
        title="Untitled Entry Ticket",
        city=None,
        category=None,
        currency="USD",
        base_price=Decimal("12.00"),
        affiliate_url="https://example.com/activity-1",
        metadata={},
    )

    mapping = store.resolve_offer(offer)
    assert mapping.source == "klook"
    assert mapping.source_activity_id == "activity-1"
    assert mapping.manual_override is False

    queue = store.list_review_queue(limit=10)
    assert len(queue) == 1
    assert queue[0].source_activity_id == "activity-1"

    store.apply_override(
        source="klook",
        source_activity_id="activity-1",
        canonical_slug="new-york-moma-general-admission",
        confidence_score=1.0,
    )

    queue_after_override = store.list_review_queue(limit=10)
    assert queue_after_override == []
