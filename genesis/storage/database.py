from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from genesis.core import DomainEvent, Experiment


class ExperimentDatabase:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.initialize()

    def initialize(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS experiments (
                id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                strategy_id TEXT NOT NULL,
                status TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL,
                completed_at TEXT
            );
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id TEXT NOT NULL,
                name TEXT NOT NULL,
                payload TEXT NOT NULL,
                timestamp TEXT NOT NULL
            );
            """
        )
        self.connection.commit()

    def save_experiment(self, experiment: Experiment) -> None:
        payload = json.dumps(experiment.to_dict(), default=str, sort_keys=True)
        self.connection.execute(
            """INSERT INTO experiments
            (id, task_id, strategy_id, status, payload, created_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              status=excluded.status, payload=excluded.payload,
              completed_at=excluded.completed_at""",
            (
                experiment.id,
                experiment.task_id,
                experiment.strategy_id,
                experiment.status.value,
                payload,
                experiment.created_at.isoformat(),
                experiment.completed_at.isoformat() if experiment.completed_at else None,
            ),
        )
        self.connection.commit()

    def append_event(self, event: DomainEvent) -> None:
        self.connection.execute(
            "INSERT INTO events (experiment_id, name, payload, timestamp) VALUES (?, ?, ?, ?)",
            (event.experiment_id, event.name, json.dumps(event.to_dict(), sort_keys=True), event.timestamp.isoformat()),
        )
        self.connection.commit()

    def get_experiment(self, experiment_id: str) -> dict[str, Any] | None:
        row = self.connection.execute("SELECT payload FROM experiments WHERE id = ?", (experiment_id,)).fetchone()
        return json.loads(row["payload"]) if row else None

    def list_experiments(self) -> list[dict[str, Any]]:
        rows = self.connection.execute("SELECT payload FROM experiments ORDER BY created_at").fetchall()
        return [json.loads(row["payload"]) for row in rows]

    def close(self) -> None:
        self.connection.close()
