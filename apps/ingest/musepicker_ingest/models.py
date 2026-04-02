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


@dataclass(frozen=True)
class AdapterResult:
    source: str
    offers: list[RawOffer]
    fetched_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
