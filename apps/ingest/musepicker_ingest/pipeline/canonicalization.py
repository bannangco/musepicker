from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path
import sqlite3

from musepicker_ingest.models import RawOffer


_SLUG_PATTERN = re.compile(r"[^a-z0-9]+")


def _slugify(value: str) -> str:
    slug = _SLUG_PATTERN.sub("-", value.lower()).strip("-")
    return slug or "unknown"


@dataclass(frozen=True)
class CanonicalMapping:
    source: str
    source_activity_id: str
    canonical_slug: str
    confidence_score: float
    manual_override: bool


class CanonicalMappingStore:
    def __init__(self, db_path: Path, review_threshold: float = 0.75) -> None:
        self.db_path = db_path
        self.review_threshold = review_threshold
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                create table if not exists source_activity_map (
                    source text not null,
                    source_activity_id text not null,
                    canonical_slug text not null,
                    confidence_score real not null,
                    manual_override integer not null default 0,
                    updated_at text not null default (datetime('now')),
                    primary key (source, source_activity_id)
                )
                """
            )
            connection.execute(
                "create index if not exists idx_source_activity_map_review on source_activity_map(manual_override, confidence_score)"
            )
            connection.commit()

    def resolve_offer(self, offer: RawOffer) -> CanonicalMapping:
        source = offer.source.strip().lower()
        source_activity_id = offer.source_activity_id.strip()

        existing = self.get(source, source_activity_id)
        if existing:
            return existing

        canonical_slug = self._build_canonical_slug(offer)
        confidence_score = self._estimate_confidence(offer)

        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                insert or ignore into source_activity_map (
                    source, source_activity_id, canonical_slug, confidence_score, manual_override, updated_at
                )
                values (?, ?, ?, ?, 0, datetime('now'))
                """,
                (source, source_activity_id, canonical_slug, confidence_score),
            )
            connection.commit()

        return self.get(source, source_activity_id) or CanonicalMapping(
            source=source,
            source_activity_id=source_activity_id,
            canonical_slug=canonical_slug,
            confidence_score=confidence_score,
            manual_override=False,
        )

    def get(self, source: str, source_activity_id: str) -> CanonicalMapping | None:
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                """
                select source, source_activity_id, canonical_slug, confidence_score, manual_override
                from source_activity_map
                where source = ? and source_activity_id = ?
                """,
                (source, source_activity_id),
            ).fetchone()
        if row is None:
            return None
        return CanonicalMapping(
            source=row[0],
            source_activity_id=row[1],
            canonical_slug=row[2],
            confidence_score=float(row[3]),
            manual_override=bool(row[4]),
        )

    def apply_override(self, source: str, source_activity_id: str, canonical_slug: str, confidence_score: float = 1.0) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                insert into source_activity_map (
                    source, source_activity_id, canonical_slug, confidence_score, manual_override, updated_at
                )
                values (?, ?, ?, ?, 1, datetime('now'))
                on conflict(source, source_activity_id) do update set
                    canonical_slug = excluded.canonical_slug,
                    confidence_score = excluded.confidence_score,
                    manual_override = 1,
                    updated_at = datetime('now')
                """,
                (source.strip().lower(), source_activity_id.strip(), canonical_slug.strip(), confidence_score),
            )
            connection.commit()

    def list_review_queue(self, limit: int = 100) -> list[CanonicalMapping]:
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                """
                select source, source_activity_id, canonical_slug, confidence_score, manual_override
                from source_activity_map
                where manual_override = 0 and confidence_score < ?
                order by confidence_score asc, updated_at asc
                limit ?
                """,
                (self.review_threshold, limit),
            ).fetchall()
        return [
            CanonicalMapping(
                source=row[0],
                source_activity_id=row[1],
                canonical_slug=row[2],
                confidence_score=float(row[3]),
                manual_override=bool(row[4]),
            )
            for row in rows
        ]

    @staticmethod
    def _build_canonical_slug(offer: RawOffer) -> str:
        pieces = [
            str(offer.city or "").strip(),
            str(offer.category or "").strip(),
            offer.title.strip(),
        ]
        return _slugify("-".join([piece for piece in pieces if piece]))

    @staticmethod
    def _estimate_confidence(offer: RawOffer) -> float:
        score = 0.45
        if offer.city:
            score += 0.15
        if offer.category:
            score += 0.10
        if offer.start_date:
            score += 0.10
        if offer.availability is not None:
            score += 0.05
        if offer.metadata:
            score += 0.10
        return min(score, 0.99)
