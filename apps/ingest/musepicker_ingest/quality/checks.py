from __future__ import annotations

from dataclasses import replace
from decimal import Decimal
import re

from musepicker_ingest.models import RawOffer


_CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")


def validate_required_fields(offer: RawOffer) -> list[str]:
    errors: list[str] = []
    if not offer.source.strip():
        errors.append("source is required")
    if not offer.source_offer_id.strip():
        errors.append("source_offer_id is required")
    if not offer.source_activity_id.strip():
        errors.append("source_activity_id is required")
    if not offer.title.strip():
        errors.append("title is required")
    if not _CURRENCY_PATTERN.match(offer.currency):
        errors.append("currency must be ISO-4217 style (e.g., USD)")
    if offer.base_price < Decimal("0"):
        errors.append("base_price must be >= 0")
    if offer.fee_amount < Decimal("0"):
        errors.append("fee_amount must be >= 0")
    if offer.discount_amount < Decimal("0"):
        errors.append("discount_amount must be >= 0")
    if not offer.affiliate_url.strip():
        errors.append("affiliate_url is required")
    return errors


def normalize_offer(offer: RawOffer) -> RawOffer:
    return replace(
        offer,
        source=offer.source.strip().lower(),
        source_offer_id=offer.source_offer_id.strip(),
        source_activity_id=offer.source_activity_id.strip(),
        title=offer.title.strip(),
        city=offer.city.strip() if isinstance(offer.city, str) else offer.city,
        category=offer.category.strip() if isinstance(offer.category, str) else offer.category,
        currency=offer.currency.strip().upper(),
        affiliate_url=offer.affiliate_url.strip()
    )


def dedupe_offers(offers: list[RawOffer]) -> list[RawOffer]:
    deduped: list[RawOffer] = []
    seen: set[str] = set()
    for offer in offers:
        key = f"{offer.source}|{offer.source_offer_id}|{offer.start_date.isoformat() if offer.start_date else 'none'}"
        if key in seen:
            continue
        seen.add(key)
        deduped.append(offer)
    return deduped


def check_data_quality(offers: list[RawOffer]) -> tuple[list[RawOffer], list[str]]:
    normalized = [normalize_offer(offer) for offer in offers]
    deduped = dedupe_offers(normalized)
    errors: list[str] = []
    for offer in deduped:
        for error in validate_required_fields(offer):
            errors.append(f"{offer.source}:{offer.source_offer_id}: {error}")
    return deduped, errors
