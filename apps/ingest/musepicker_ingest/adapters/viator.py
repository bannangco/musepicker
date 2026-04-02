from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path

from musepicker_ingest.adapters.base import SourceAdapter
from musepicker_ingest.adapters.common import fetch_json, load_json_file, normalize_currency, parse_date, to_decimal, utcnow
from musepicker_ingest.models import AdapterResult, RawOffer


class ViatorAdapter(SourceAdapter):
    source_name = "viator"

    def __init__(self, fixture_path: Path | None = None, api_url: str | None = None) -> None:
        super().__init__(fixture_path=fixture_path)
        self.api_url = api_url or os.getenv("VIATOR_API_URL")
        self.api_key = os.getenv("VIATOR_API_KEY")

    def fetch_raw_offers(self, since: datetime | None = None) -> AdapterResult:
        payload = self._load_payload()
        observed_at = utcnow()
        offers: list[RawOffer] = []

        source_items = payload.get("offers", []) if isinstance(payload, dict) else payload
        if not isinstance(source_items, list):
            raise ValueError("Viator payload must be a list or object with offers list")

        for index, item in enumerate(source_items):
            if not isinstance(item, dict):
                continue
            source_offer_id = str(item.get("offer_id") or item.get("id") or f"viator-{index}")
            source_activity_id = str(item.get("activity_id") or source_offer_id)
            title = str(item.get("title") or item.get("name") or "").strip()
            affiliate_url = str(item.get("affiliate_url") or item.get("url") or "").strip()
            if not title or not affiliate_url:
                continue

            offers.append(
                RawOffer(
                    source=self.source_name,
                    source_offer_id=source_offer_id,
                    source_activity_id=source_activity_id,
                    title=title,
                    city=item.get("city"),
                    category=item.get("category"),
                    currency=normalize_currency(item.get("currency") or "USD"),
                    base_price=to_decimal(item.get("base_price")),
                    fee_amount=to_decimal(item.get("fee_amount")),
                    discount_amount=to_decimal(item.get("discount_amount")),
                    availability=int(item["availability"]) if item.get("availability") is not None else None,
                    start_date=parse_date(item.get("start_date")),
                    affiliate_url=affiliate_url,
                    metadata={"raw": item},
                    observed_at=observed_at
                )
            )

        return AdapterResult(source=self.source_name, offers=offers, fetched_at=observed_at, metadata={"count": len(offers)})

    def _load_payload(self):
        if self.fixture_path:
            return load_json_file(self.fixture_path)

        if self.api_url:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None
            return fetch_json(self.api_url, headers=headers)

        raise RuntimeError("Viator adapter requires either fixture_path or VIATOR_API_URL")
