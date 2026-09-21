from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class StrategyMemoryEntry:
    task_signature: str
    strategy_id: str
    outcome: str
    score: float
    lesson: str
    failure_fingerprint: str = ""


class StrategyMemory:
    """Small persistent memory that turns outcomes into retrievable lessons."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else None
        self.entries: list[StrategyMemoryEntry] = []
        if self.path and self.path.exists():
            self.entries = [StrategyMemoryEntry(**item) for item in json.loads(self.path.read_text(encoding="utf-8"))]

    def record(self, entry: StrategyMemoryEntry) -> None:
        self.entries.append(entry)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps([asdict(item) for item in self.entries], indent=2) + "\n", encoding="utf-8")

    def recall(self, task_signature: str, limit: int = 5) -> tuple[StrategyMemoryEntry, ...]:
        matches = [entry for entry in self.entries if entry.task_signature == task_signature]
        return tuple(sorted(matches, key=lambda item: item.score, reverse=True)[:limit])

    def lessons_for(self, task_signature: str) -> tuple[str, ...]:
        return tuple(entry.lesson for entry in self.recall(task_signature) if entry.lesson.strip())
