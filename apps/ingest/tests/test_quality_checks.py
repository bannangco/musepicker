from decimal import Decimal

from musepicker_ingest.models import RawOffer
from musepicker_ingest.quality.checks import check_data_quality, validate_required_fields


def _build_offer(**overrides):
    payload = {
        "source": "klook",
        "source_offer_id": "offer-123",
        "source_activity_id": "activity-123",
        "title": "MoMA Ticket",
        "city": "New York",
        "category": "Museums & Galleries",
        "currency": "USD",
        "base_price": Decimal("20.00"),
        "fee_amount": Decimal("1.00"),
        "discount_amount": Decimal("0"),
        "affiliate_url": "https://example.com/book",
    }
    payload.update(overrides)
    return RawOffer(**payload)


def test_validate_required_fields_passes_valid_offer():
    offer = _build_offer()
    errors = validate_required_fields(offer)
    assert errors == []


def test_validate_required_fields_detects_invalid_currency():
    offer = _build_offer(currency="US$")
    errors = validate_required_fields(offer)
    assert any("currency" in item for item in errors)


def test_data_quality_deduplicates_same_offer():
    first = _build_offer()
    second = _build_offer()
    cleaned, errors = check_data_quality([first, second])
    assert len(cleaned) == 1
    assert errors == []
