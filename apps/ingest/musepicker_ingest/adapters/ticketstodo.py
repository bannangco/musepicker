from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path
from urllib.parse import urlparse

from musepicker_ingest.adapters.base import SourceAdapter
from musepicker_ingest.adapters.common import fetch_json, load_json_file, normalize_currency, to_decimal, utcnow
from musepicker_ingest.models import AdapterResult, RawOffer


def _slug_from_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed.path.strip("/").replace("/", "-") or url


class TicketsToDoAdapter(SourceAdapter):
    source_name = "ticketstodo"

    def __init__(self, fixture_path: Path | None = None, api_url: str | None = None) -> None:
        super().__init__(fixture_path=fixture_path)
        self.api_url = api_url or os.getenv("TICKETSTODO_API_URL")
        self.api_key = os.getenv("TICKETSTODO_API_KEY")

    def fetch_raw_offers(self, since: datetime | None = None) -> AdapterResult:
        payload = self._load_payload()
        observed_at = utcnow()
        offers: list[RawOffer] = []

        if isinstance(payload, list):
            for index, item in enumerate(payload):
                offers.extend(self._offers_from_item(item, index, observed_at))
        elif isinstance(payload, dict) and isinstance(payload.get("offers"), list):
            for index, item in enumerate(payload["offers"]):
                offers.extend(self._offers_from_item(item, index, observed_at))
        else:
            raise ValueError("TicketsToDo payload must be a list or object with offers list")

        return AdapterResult(source=self.source_name, offers=offers, fetched_at=observed_at, metadata={"count": len(offers)})

    def _offers_from_item(self, item: dict, index: int, observed_at: datetime) -> list[RawOffer]:
        if not isinstance(item, dict):
            return []

        title = str(item.get("title") or item.get("name") or "").strip()
        list_url = str(item.get("list_url") or item.get("url") or "").strip()
        book_url = str(item.get("book_now_url") or list_url).strip()

        if not title or not book_url:
            return []

        pricing = item.get("pricing") if isinstance(item.get("pricing"), dict) else {}
        discounted = pricing.get("discounted_price")
        original = pricing.get("original_price")
        base_price = to_decimal(discounted if discounted is not None else original)
        if base_price <= 0:
            base_price = to_decimal(item.get("price"))

        offer_id = _slug_from_url(book_url or list_url) or f"ticketstodo-{index}"
        source_activity_id = _slug_from_url(list_url) if list_url else offer_id

        return [
            RawOffer(
                source=self.source_name,
                source_offer_id=offer_id,
                source_activity_id=source_activity_id,
                title=title,
                city="New York",
                category="Museums & Galleries",
                currency=normalize_currency(item.get("currency") or "USD"),
                base_price=base_price,
                fee_amount=to_decimal("0"),
                discount_amount=to_decimal("0"),
                availability=None,
                start_date=None,
                affiliate_url=book_url,
                metadata={
                    "description": item.get("description"),
                    "location": item.get("location"),
                    "discount": pricing.get("discount")
                },
                observed_at=observed_at
            )
        ]

    def _load_payload(self):
        if self.fixture_path:
            return load_json_file(self.fixture_path)

        if self.api_url:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None
            return fetch_json(self.api_url, headers=headers)

        raise RuntimeError("TicketsToDo adapter requires either fixture_path or TICKETSTODO_API_URL")
