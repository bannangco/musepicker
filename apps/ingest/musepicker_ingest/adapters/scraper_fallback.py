from __future__ import annotations

from datetime import datetime
from pathlib import Path

from musepicker_ingest.adapters.base import SourceAdapter
from musepicker_ingest.adapters.common import load_json_file, normalize_currency, parse_date, to_decimal, utcnow
from musepicker_ingest.models import AdapterResult, RawOffer


class ScraperFallbackAdapter(SourceAdapter):
    source_name = "scraper_fallback"

    def __init__(self, fixture_path: Path) -> None:
        super().__init__(fixture_path=fixture_path)

    def fetch_raw_offers(self, since: datetime | None = None) -> AdapterResult:
        if not self.fixture_path:
            raise RuntimeError("Scraper fallback requires fixture_path")

        payload = load_json_file(self.fixture_path)
        observed_at = utcnow()
        offers: list[RawOffer] = []

        source_items = []
        if isinstance(payload, dict) and isinstance(payload.get("museums"), list):
            source_items = payload["museums"]
        elif isinstance(payload, list):
            source_items = payload
        else:
            raise ValueError("Fallback payload must be list or object with museums list")

        for index, item in enumerate(source_items):
            if not isinstance(item, dict):
                continue

            title = str(item.get("title") or item.get("name") or "").strip()
            url = str(item.get("affiliate_url") or item.get("url") or "").strip()
            if not title or not url:
                continue

            offer_id = str(item.get("source_offer_id") or item.get("id") or f"fallback-{index}")
            source_activity_id = str(item.get("source_activity_id") or item.get("activity_id") or offer_id)

            offers.append(
                RawOffer(
                    source=self.source_name,
                    source_offer_id=offer_id,
                    source_activity_id=source_activity_id,
                    title=title,
                    city=item.get("city"),
                    category=item.get("category"),
                    currency=normalize_currency(item.get("currency") or "USD"),
                    base_price=to_decimal(item.get("base_price") or item.get("price")),
                    fee_amount=to_decimal(item.get("fee_amount")),
                    discount_amount=to_decimal(item.get("discount_amount")),
                    availability=int(item["availability"]) if item.get("availability") is not None else None,
                    start_date=parse_date(item.get("start_date")),
                    affiliate_url=url,
                    metadata={"raw": item},
                    observed_at=observed_at
                )
            )

        return AdapterResult(source=self.source_name, offers=offers, fetched_at=observed_at, metadata={"count": len(offers)})
