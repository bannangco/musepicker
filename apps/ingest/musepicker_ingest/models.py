from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal
import hashlib
from typing import Any


@dataclass(frozen=True)
class RawOffer:
    source: str
    source_offer_id: str
    source_activity_id: str
    title: str
    city: str | None
    category: str | None
    currency: str
    base_price: Decimal
    fee_amount: Decimal = Decimal("0")
    discount_amount: Decimal = Decimal("0")
    availability: int | None = None
    start_date: date | None = None
    affiliate_url: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    observed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def effective_price(self) -> Decimal:
        return self.base_price + self.fee_amount - self.discount_amount

    def idempotency_key(self) -> str:
        key = "|".join(
            [
                self.source.strip().lower(),
                self.source_offer_id.strip(),
                self.source_activity_id.strip(),
                self.currency.strip().upper(),
                f"{self.base_price:.2f}",
                self.start_date.isoformat() if self.start_date else "none"
            ]
        )
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "source_offer_id": self.source_offer_id,
            "source_activity_id": self.source_activity_id,
            "title": self.title,
            "city": self.city,
            "category": self.category,
            "currency": self.currency,
            "base_price": f"{self.base_price:.2f}",
            "fee_amount": f"{self.fee_amount:.2f}",
            "discount_amount": f"{self.discount_amount:.2f}",
            "effective_price": f"{self.effective_price:.2f}",
            "availability": self.availability,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "affiliate_url": self.affiliate_url,
            "metadata": self.metadata,
            "observed_at": self.observed_at.isoformat()
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RawOffer":
        if not isinstance(payload, dict):
            raise ValueError("payload must be an object")

        observed_at_raw = payload.get("observed_at")
        observed_at = datetime.now(timezone.utc)
        if isinstance(observed_at_raw, str) and observed_at_raw.strip():
            observed_at = datetime.fromisoformat(observed_at_raw.replace("Z", "+00:00"))

        start_date_raw = payload.get("start_date")
        parsed_start_date: date | None = None
        if isinstance(start_date_raw, str) and start_date_raw.strip():
            parsed_start_date = date.fromisoformat(start_date_raw)

        availability_raw = payload.get("availability")
        availability: int | None = None
        if availability_raw is not None and availability_raw != "":
            availability = int(availability_raw)

        return cls(
            source=str(payload.get("source") or ""),
            source_offer_id=str(payload.get("source_offer_id") or ""),
            source_activity_id=str(payload.get("source_activity_id") or ""),
            title=str(payload.get("title") or ""),
            city=payload.get("city"),
            category=payload.get("category"),
            currency=str(payload.get("currency") or ""),
            base_price=Decimal(str(payload.get("base_price") or "0")),
            fee_amount=Decimal(str(payload.get("fee_amount") or "0")),
            discount_amount=Decimal(str(payload.get("discount_amount") or "0")),
            availability=availability,
            start_date=parsed_start_date,
            affiliate_url=str(payload.get("affiliate_url") or ""),
            metadata=payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {},
            observed_at=observed_at
        )


@dataclass(frozen=True)
class AdapterResult:
    source: str
    offers: list[RawOffer]
    fetched_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
