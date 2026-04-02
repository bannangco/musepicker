from __future__ import annotations

import sqlite3
from pathlib import Path


class IdempotencyStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                create table if not exists processed_keys (
                    idempotency_key text primary key,
                    run_id text not null,
                    created_at text not null default (datetime('now'))
                )
                """
            )
            connection.commit()

    def has(self, idempotency_key: str) -> bool:
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                "select 1 from processed_keys where idempotency_key = ? limit 1",
                (idempotency_key,),
            ).fetchone()
            return row is not None

    def mark(self, idempotency_key: str, run_id: str) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                insert or ignore into processed_keys (idempotency_key, run_id)
                values (?, ?)
                """,
                (idempotency_key, run_id),
            )
            connection.commit()
