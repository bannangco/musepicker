from pathlib import Path

from musepicker_ingest.adapters.klook import KlookAdapter
from musepicker_ingest.adapters.scraper_fallback import ScraperFallbackAdapter
from musepicker_ingest.adapters.ticketstodo import TicketsToDoAdapter
from musepicker_ingest.adapters.tripcom import TripComAdapter
from musepicker_ingest.adapters.viator import ViatorAdapter


FIXTURES = Path(__file__).parent / "fixtures"


def _assert_offer_shape(offer):
    assert offer.source
    assert offer.source_offer_id
    assert offer.source_activity_id
    assert offer.title
    assert offer.currency
    assert offer.base_price >= 0
    assert offer.affiliate_url
    assert offer.observed_at is not None


def test_klook_contract():
    adapter = KlookAdapter(fixture_path=FIXTURES / "klook_museum_list.sample.json")
    result = adapter.fetch_raw_offers()
    assert result.source == "klook"
    assert len(result.offers) == 2
    for offer in result.offers:
        _assert_offer_shape(offer)


def test_ticketstodo_contract():
    adapter = TicketsToDoAdapter(fixture_path=FIXTURES / "ticketstodo_museum_details.sample.json")
    result = adapter.fetch_raw_offers()
    assert result.source == "ticketstodo"
    assert len(result.offers) == 2
    for offer in result.offers:
        _assert_offer_shape(offer)


def test_tripcom_contract():
    adapter = TripComAdapter(fixture_path=FIXTURES / "tripcom_offers.sample.json")
    result = adapter.fetch_raw_offers()
    assert result.source == "tripcom"
    assert len(result.offers) == 1
    _assert_offer_shape(result.offers[0])


def test_viator_contract():
    adapter = ViatorAdapter(fixture_path=FIXTURES / "viator_offers.sample.json")
    result = adapter.fetch_raw_offers()
    assert result.source == "viator"
    assert len(result.offers) == 1
    _assert_offer_shape(result.offers[0])


def test_fallback_contract():
    adapter = ScraperFallbackAdapter(fixture_path=FIXTURES / "fallback_offers.sample.json")
    result = adapter.fetch_raw_offers()
    assert result.source == "scraper_fallback"
    assert len(result.offers) == 1
    _assert_offer_shape(result.offers[0])
