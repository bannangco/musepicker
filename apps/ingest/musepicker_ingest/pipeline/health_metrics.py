from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


class HealthMetricsStore:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def update(self, source: str, updates: dict[str, Any]) -> Path:
        metrics_file = self.root_dir / f"{source}.json"
        existing: dict[str, Any] = {}
        if metrics_file.exists():
            with metrics_file.open("r", encoding="utf-8") as handle:
                existing = json.load(handle)

        success_increment = int(updates.pop("success_increment", 0))
        failure_increment = int(updates.pop("failure_increment", 0))

        merged = {
            "source": source,
            "last_run_at": datetime.now(timezone.utc).isoformat(),
            "total_runs": int(existing.get("total_runs", 0)) + 1,
            "total_successes": int(existing.get("total_successes", 0)),
            "total_failures": int(existing.get("total_failures", 0)),
            "last_status": existing.get("last_status", "unknown"),
            "last_accepted": int(existing.get("last_accepted", 0)),
            "last_duplicates": int(existing.get("last_duplicates", 0)),
            "last_invalid": int(existing.get("last_invalid", 0))
        }
        merged["total_successes"] += success_increment
        merged["total_failures"] += failure_increment
        merged.update(updates)

        with metrics_file.open("w", encoding="utf-8") as handle:
            json.dump(merged, handle, ensure_ascii=False, indent=2)
        return metrics_file
