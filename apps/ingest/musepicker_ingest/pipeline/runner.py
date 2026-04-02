from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import logging
import time
import traceback
from typing import Iterable
from uuid import uuid4

from musepicker_ingest.adapters.base import SourceAdapter
from musepicker_ingest.config import IngestConfig
from musepicker_ingest.models import RawOffer
from musepicker_ingest.pipeline.canonicalization import CanonicalMappingStore
from musepicker_ingest.pipeline.dead_letter import DeadLetterStore
from musepicker_ingest.pipeline.health_metrics import HealthMetricsStore
from musepicker_ingest.pipeline.idempotency import IdempotencyStore
from musepicker_ingest.pipeline.storage import RunLogStore, SnapshotStore
from musepicker_ingest.quality.checks import evaluate_offers


@dataclass
class SourceRunStats:
    source: str
    fetched: int = 0
    accepted: int = 0
    duplicates: int = 0
    invalid: int = 0
    dead_letters: int = 0
    canonical_mapped: int = 0
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
        self.dead_letters = DeadLetterStore(self.config.state_dir / "dead_letters.sqlite3")
        self.canonicalization = CanonicalMappingStore(self.config.state_dir / "canonicalization.sqlite3")
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
        last_exception: Exception | None = None

        for attempt in range(1, self.config.retries + 1):
            try:
                result = adapter.fetch_raw_offers()
                stats.retries = attempt - 1
                offers, rejected_offers, quality_errors = evaluate_offers(result.offers)
                stats.fetched = len(result.offers)
                stats.invalid = len(rejected_offers)
                stats.errors.extend(quality_errors)

                if not dry_run:
                    for rejected in rejected_offers:
                        self.dead_letters.add(
                            source=adapter.source_name,
                            run_id=run_id,
                            reason="quality_validation_failed",
                            payload={
                                "offer": rejected.offer.to_dict(),
                                "errors": rejected.errors
                            }
                        )
                        stats.dead_letters += 1

                for offer in offers:
                    if self._accept_offer(run_id, offer, dry_run=dry_run):
                        stats.accepted += 1
                        if not dry_run:
                            self.canonicalization.resolve_offer(offer)
                            stats.canonical_mapped += 1
                    else:
                        stats.duplicates += 1
                self._update_health(stats)
                return stats
            except Exception as exc:  # noqa: BLE001
                last_exception = exc
                stats.retries = attempt
                stats.status = "failed"
                error = f"Attempt {attempt} failed: {exc}"
                stats.errors.append(error)
                self.logger.error("%s\n%s", error, traceback.format_exc())
                if attempt < self.config.retries:
                    sleep_seconds = self.config.initial_backoff_seconds * (2 ** (attempt - 1))
                    time.sleep(sleep_seconds)

        if not dry_run and last_exception is not None:
            self.dead_letters.add(
                source=adapter.source_name,
                run_id=run_id,
                reason="adapter_fetch_failed",
                payload={"source": adapter.source_name, "error": str(last_exception)}
            )
            stats.dead_letters += 1
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
            "last_invalid": stats.invalid,
            "last_dead_letters": stats.dead_letters,
            "last_canonical_mapped": stats.canonical_mapped
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

    def replay_dead_letters(self, source: str | None = None, limit: int = 100, dry_run: bool = False) -> dict:
        run_id = f"replay-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:8]}"
        entries = self.dead_letters.list_unreplayed(source=source, limit=limit)
        stats_by_source: dict[str, SourceRunStats] = {}

        self.logger.info("Starting replay run %s for %d dead-letter entries", run_id, len(entries))
        for entry in entries:
            stats = stats_by_source.setdefault(entry.source, SourceRunStats(source=entry.source))
            stats.fetched += 1
            payload = entry.payload
            if isinstance(payload, dict) and isinstance(payload.get("offer"), dict):
                payload = payload["offer"]

            try:
                offer = RawOffer.from_dict(payload)
            except Exception as exc:  # noqa: BLE001
                stats.invalid += 1
                stats.status = "failed"
                stats.errors.append(f"Failed to parse dead-letter payload ({entry.id}): {exc}")
                continue

            try:
                if self._accept_offer(run_id, offer, dry_run=dry_run):
                    stats.accepted += 1
                    if not dry_run:
                        self.canonicalization.resolve_offer(offer)
                        stats.canonical_mapped += 1
                else:
                    stats.duplicates += 1
                if not dry_run:
                    self.dead_letters.mark_replayed(entry.id, run_id)
            except Exception as exc:  # noqa: BLE001
                stats.status = "failed"
                stats.errors.append(f"Replay failed for {entry.id}: {exc}")
                self.logger.error("Replay failed for %s: %s", entry.id, exc)

        for stats in stats_by_source.values():
            self._update_health(stats)

        summary = {
            "run_id": run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dry_run": dry_run,
            "replay": True,
            "replayed_entries": len(entries),
            "sources": [asdict(stats) for stats in stats_by_source.values()]
        }
        run_log_path = self.run_logs.write_run_summary(run_id, summary)
        self.logger.info("Finished replay run %s (log=%s)", run_id, run_log_path)
        return summary
