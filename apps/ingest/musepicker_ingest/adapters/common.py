from __future__ import annotations

from datetime import datetime, date, timezone
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re
from typing import Any

import requests


PRICE_PATTERN = re.compile(r"([A-Za-z$]+)?\s*([0-9]+(?:[.,][0-9]{1,2})?)")


def load_json_file(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fetch_json(api_url: str, headers: dict[str, str] | None = None) -> Any:
    response = requests.get(api_url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()


def to_decimal(value: Any) -> Decimal:
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))

    raw = str(value).strip()
    if not raw:
        return Decimal("0")

    match = PRICE_PATTERN.search(raw.replace(",", ""))
    if not match:
        return Decimal("0")

    number_part = match.group(2)
    try:
        return Decimal(number_part)
    except InvalidOperation:
        return Decimal("0")


def normalize_currency(value: Any, fallback: str = "USD") -> str:
    if value is None:
        return fallback

    raw = str(value).strip().upper()
    if not raw:
        return fallback

    synonyms = {
        "US$": "USD",
        "$": "USD",
        "USD$": "USD",
        "US DOLLAR": "USD"
    }
    if raw in synonyms:
        return synonyms[raw]
    if len(raw) == 3 and raw.isalpha():
        return raw
    return fallback


def parse_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    raw = str(value).strip()
    if not raw:
        return None
    try:
        if "T" in raw:
            return datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
        return date.fromisoformat(raw)
    except ValueError:
        return None


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
