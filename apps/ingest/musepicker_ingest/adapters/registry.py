from __future__ import annotations

from pathlib import Path

from musepicker_ingest.adapters.base import SourceAdapter
from musepicker_ingest.adapters.klook import KlookAdapter
from musepicker_ingest.adapters.ticketstodo import TicketsToDoAdapter
from musepicker_ingest.adapters.tripcom import TripComAdapter
from musepicker_ingest.adapters.viator import ViatorAdapter


def create_api_first_adapters(fixtures: dict[str, Path] | None = None) -> dict[str, SourceAdapter]:
    fixtures = fixtures or {}
    return {
        "klook": KlookAdapter(fixture_path=fixtures.get("klook")),
        "tripcom": TripComAdapter(fixture_path=fixtures.get("tripcom")),
        "ticketstodo": TicketsToDoAdapter(fixture_path=fixtures.get("ticketstodo")),
        "viator": ViatorAdapter(fixture_path=fixtures.get("viator"))
    }
