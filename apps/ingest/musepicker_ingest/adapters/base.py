from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from musepicker_ingest.models import AdapterResult


class SourceAdapter(ABC):
    source_name: str

    def __init__(self, fixture_path: Path | None = None) -> None:
        self.fixture_path = fixture_path

    @abstractmethod
    def fetch_raw_offers(self, since: datetime | None = None) -> AdapterResult:
        raise NotImplementedError
