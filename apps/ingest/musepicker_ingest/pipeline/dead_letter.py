from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import sqlite3
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class DeadLetterEntry:
    id: str
    source: str
    run_id: str
    reason: str
    payload: dict[str, Any]
    created_at: str
    replayed_at: str | None


class DeadLetterStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                create table if not exists dead_letters (
                    id text primary key,
                    source text not null,
                    run_id text not null,
                    reason text not null,
                    payload_json text not null,
                    created_at text not null default (datetime('now')),
                    replayed_at text,
                    replay_run_id text
                )
                """
            )
            connection.execute("create index if not exists idx_dead_letters_source on dead_letters(source)")
            connection.execute("create index if not exists idx_dead_letters_replayed on dead_letters(replayed_at)")
            connection.commit()

    def add(self, source: str, run_id: str, reason: str, payload: dict[str, Any]) -> str:
        entry_id = str(uuid4())
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                insert into dead_letters (id, source, run_id, reason, payload_json)
                values (?, ?, ?, ?, ?)
                """,
                (entry_id, source, run_id, reason, json.dumps(payload, ensure_ascii=False)),
            )
            connection.commit()
        return entry_id

    def list_unreplayed(self, source: str | None = None, limit: int = 100) -> list[DeadLetterEntry]:
        query = """
            select id, source, run_id, reason, payload_json, created_at, replayed_at
            from dead_letters
            where replayed_at is null
        """
        params: tuple[Any, ...] = ()
        if source:
            query += " and source = ?"
            params += (source,)
        query += " order by created_at asc limit ?"
        params += (limit,)

        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(query, params).fetchall()

        return [
            DeadLetterEntry(
                id=row[0],
                source=row[1],
                run_id=row[2],
                reason=row[3],
                payload=json.loads(row[4]),
                created_at=row[5],
                replayed_at=row[6],
            )
            for row in rows
        ]

    def mark_replayed(self, entry_id: str, replay_run_id: str) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                update dead_letters
                set replayed_at = datetime('now'),
                    replay_run_id = ?
                where id = ?
                """,
                (replay_run_id, entry_id),
            )
            connection.commit()
