from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path
from urllib.parse import urlparse

from musepicker_ingest.adapters.base import SourceAdapter
from musepicker_ingest.adapters.common import fetch_json, load_json_file, normalize_currency, to_decimal, utcnow
from musepicker_ingest.models import AdapterResult, RawOffer


def _offer_id_from_url(url: str) -> str:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    return parts[1] if len(parts) > 1 else parsed.path or url


class KlookAdapter(SourceAdapter):
    source_name = "klook"

    def __init__(self, fixture_path: Path | None = None, api_url: str | None = None) -> None:
        super().__init__(fixture_path=fixture_path)
        self.api_url = api_url or os.getenv("KLOOK_API_URL")
        self.api_key = os.getenv("KLOOK_API_KEY")

    def fetch_raw_offers(self, since: datetime | None = None) -> AdapterResult:
        payload = self._load_payload()
        museums = payload.get("museums", []) if isinstance(payload, dict) else []
        observed_at = utcnow()
        offers: list[RawOffer] = []

        for museum in museums:
            url = str(museum.get("url") or "").strip()
            title = str(museum.get("title") or "").strip()
            if not url or not title:
                continue

            raw_price = museum.get("price")
            currency_hint = "US$" if str(raw_price).strip().startswith("US$") else "USD"
            offer_id = _offer_id_from_url(url)

            offers.append(
                RawOffer(
                    source=self.source_name,
                    source_offer_id=offer_id,
                    source_activity_id=offer_id,
                    title=title,
                    city="New York",
                    category="Museums & Galleries",
                    currency=normalize_currency(currency_hint),
                    base_price=to_decimal(raw_price),
                    fee_amount=to_decimal("0"),
                    discount_amount=to_decimal("0"),
                    availability=None,
                    start_date=None,
                    affiliate_url=url,
                    metadata={
                        "rating": museum.get("rating"),
                        "reviews": museum.get("reviews"),
                        "image_url": museum.get("image_url")
                    },
                    observed_at=observed_at
                )
            )

        return AdapterResult(source=self.source_name, offers=offers, fetched_at=observed_at, metadata={"count": len(offers)})

    def _load_payload(self) -> dict:
        if self.fixture_path:
            payload = load_json_file(self.fixture_path)
            if not isinstance(payload, dict):
                raise ValueError("Klook fixture must be an object with a museums array")
            return payload

        if self.api_url:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None
            payload = fetch_json(self.api_url, headers=headers)
            if not isinstance(payload, dict):
                raise ValueError("Klook API response must be an object")
            return payload

        raise RuntimeError("Klook adapter requires either fixture_path or KLOOK_API_URL")
