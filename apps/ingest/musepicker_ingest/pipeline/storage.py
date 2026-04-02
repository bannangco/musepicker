from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from musepicker_ingest.models import RawOffer


def _json_default(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


class SnapshotStore:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def append_offer(self, offer: RawOffer) -> Path:
        timestamp = datetime.now(timezone.utc)
        day_path = self.root_dir / offer.source / timestamp.strftime("%Y-%m-%d")
        day_path.mkdir(parents=True, exist_ok=True)
        snapshot_file = day_path / "offers.jsonl"
        with snapshot_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(offer.to_dict(), ensure_ascii=False, default=_json_default) + "\n")
        return snapshot_file


class RunLogStore:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def write_run_summary(self, run_id: str, payload: dict[str, Any]) -> Path:
        run_file = self.root_dir / f"{run_id}.json"
        with run_file.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, default=_json_default)
        return run_file
