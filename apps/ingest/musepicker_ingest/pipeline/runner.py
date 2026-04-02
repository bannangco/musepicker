from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import logging
from pathlib import Path
import time
import traceback
from typing import Iterable
from uuid import uuid4

from musepicker_ingest.adapters.base import SourceAdapter
from musepicker_ingest.config import IngestConfig
from musepicker_ingest.models import RawOffer
from musepicker_ingest.pipeline.health_metrics import HealthMetricsStore
from musepicker_ingest.pipeline.idempotency import IdempotencyStore
from musepicker_ingest.pipeline.storage import RunLogStore, SnapshotStore
from musepicker_ingest.quality.checks import check_data_quality


@dataclass
class SourceRunStats:
    source: str
    fetched: int = 0
    accepted: int = 0
    duplicates: int = 0
    invalid: int = 0
    retries: int = 0
    status: str = "success"
    errors: list[str] = None

    def __post_init__(self) -> None:
        if self.errors is None:
            self.errors = []


class IngestRunner:
    def __init__(self, config: IngestConfig, adapters: Iterable[SourceAdapter]) -> None:
        self.config = config
        self.adapters = {adapter.source_name: adapter for adapter in adapters}

        self.config.state_dir.mkdir(parents=True, exist_ok=True)
        self.config.snapshots_dir.mkdir(parents=True, exist_ok=True)
        self.config.runs_dir.mkdir(parents=True, exist_ok=True)
        self.config.metrics_dir.mkdir(parents=True, exist_ok=True)

        self.idempotency = IdempotencyStore(self.config.state_dir / "idempotency.sqlite3")
        self.snapshots = SnapshotStore(self.config.snapshots_dir)
        self.run_logs = RunLogStore(self.config.runs_dir)
        self.metrics = HealthMetricsStore(self.config.metrics_dir)

        logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
        self.logger = logging.getLogger("musepicker_ingest")

    def run(self, source: str | None = None, dry_run: bool = False) -> dict:
        run_id = f"run-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:8]}"
        selected_adapters = self._select_adapters(source)
        source_stats: list[SourceRunStats] = []

        self.logger.info("Starting ingest run %s for sources=%s", run_id, [a.source_name for a in selected_adapters])

        for adapter in selected_adapters:
            source_stats.append(self._run_one_adapter(run_id, adapter, dry_run=dry_run))

        summary = {
            "run_id": run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dry_run": dry_run,
            "sources": [asdict(stats) for stats in source_stats]
        }
        run_log_path = self.run_logs.write_run_summary(run_id, summary)
        self.logger.info("Finished ingest run %s (log=%s)", run_id, run_log_path)
        return summary

    def _run_one_adapter(self, run_id: str, adapter: SourceAdapter, dry_run: bool) -> SourceRunStats:
        stats = SourceRunStats(source=adapter.source_name)

        for attempt in range(1, self.config.retries + 1):
            try:
                result = adapter.fetch_raw_offers()
                stats.retries = attempt - 1
                offers, quality_errors = check_data_quality(result.offers)
                stats.fetched = len(result.offers)
                stats.invalid = len(quality_errors)
                stats.errors.extend(quality_errors)

                for offer in offers:
                    if self._accept_offer(run_id, offer, dry_run=dry_run):
                        stats.accepted += 1
                    else:
                        stats.duplicates += 1
                self._update_health(stats)
                return stats
            except Exception as exc:  # noqa: BLE001
                stats.retries = attempt
                stats.status = "failed"
                error = f"Attempt {attempt} failed: {exc}"
                stats.errors.append(error)
                self.logger.error("%s\n%s", error, traceback.format_exc())
                if attempt < self.config.retries:
                    sleep_seconds = self.config.initial_backoff_seconds * (2 ** (attempt - 1))
                    time.sleep(sleep_seconds)

        self._update_health(stats)
        return stats

    def _accept_offer(self, run_id: str, offer: RawOffer, dry_run: bool) -> bool:
        key = offer.idempotency_key()
        if self.idempotency.has(key):
            return False
        if not dry_run:
            self.snapshots.append_offer(offer)
            self.idempotency.mark(key, run_id)
        return True

    def _update_health(self, stats: SourceRunStats) -> None:
        updates = {
            "last_status": stats.status,
            "last_accepted": stats.accepted,
            "last_duplicates": stats.duplicates,
            "last_invalid": stats.invalid
        }
        if stats.status == "success":
            updates["success_increment"] = 1
        else:
            updates["failure_increment"] = 1
        self.metrics.update(stats.source, updates)

    def _select_adapters(self, source: str | None) -> list[SourceAdapter]:
        if source is None:
            return list(self.adapters.values())
        if source not in self.adapters:
            raise ValueError(f"Unknown source '{source}'. Available: {sorted(self.adapters.keys())}")
        return [self.adapters[source]]
