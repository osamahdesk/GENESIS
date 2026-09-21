"""Typed domain models for GENESIS experiments.

These models contain data and validation only. Orchestration and event handling
belong to later implementation days.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


def utc_now() -> datetime:
    return datetime.now(UTC)


class ExperimentStatus(StrEnum):
    CREATED = "created"
    RESEARCHING = "researching"
    BUILDING = "building"
    EXECUTING = "executing"
    EVALUATING = "evaluating"
    CRITIQUING = "critiquing"
    STORED = "stored"
    VERIFIED = "verified"
    REJECTED = "rejected"
    FAILED = "failed"
    BUDGET_EXCEEDED = "budget_exceeded"


class ArtifactKind(StrEnum):
    SOURCE = "source"
    TEST = "test"
    LOG = "log"
    REPORT = "report"
    BUNDLE = "bundle"


@dataclass(frozen=True, slots=True)
class Task:
    """An immutable problem definition used by an experiment."""

    id: str
    name: str
    statement: str
    benchmark_version: str
    development_cases: tuple[str, ...] = ()
    validation_cases: tuple[str, ...] = ()
    hidden_cases: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.id, "Task.id")
        _require_text(self.name, "Task.name")
        _require_text(self.statement, "Task.statement")
        _require_text(self.benchmark_version, "Task.benchmark_version")
        if not self.development_cases and not self.validation_cases and not self.hidden_cases:
            raise ValueError("Task must contain at least one evaluation case")


@dataclass(frozen=True, slots=True)
class Strategy:
    """A versioned workflow description; it is not executable authority."""

    id: str
    name: str
    version: str
    steps: tuple[str, ...]
    parent_id: str | None = None
    prompt_refs: tuple[str, ...] = ()
    max_retries: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.id, "Strategy.id")
        _require_text(self.name, "Strategy.name")
        _require_text(self.version, "Strategy.version")
        if not self.steps or any(not step.strip() for step in self.steps):
            raise ValueError("Strategy.steps must contain non-empty steps")
        if self.max_retries < 0:
            raise ValueError("Strategy.max_retries cannot be negative")


@dataclass(frozen=True, slots=True)
class Budget:
    """Hard limits assigned to one experiment."""

    max_runtime_seconds: int = 60
    max_model_calls: int = 10
    max_retries: int = 1
    max_tokens: int | None = None
    max_memory_mb: int | None = None
    max_disk_mb: int | None = None

    def __post_init__(self) -> None:
        for name in (
            "max_runtime_seconds",
            "max_model_calls",
            "max_retries",
            "max_tokens",
            "max_memory_mb",
            "max_disk_mb",
        ):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise ValueError(f"Budget.{name} cannot be negative")
        if self.max_runtime_seconds == 0:
            raise ValueError("Budget.max_runtime_seconds must be positive")


@dataclass(frozen=True, slots=True)
class ArtifactRef:
    id: str
    path: str
    kind: ArtifactKind
    content_hash: str
    producer: str

    def __post_init__(self) -> None:
        for name in ("id", "path", "content_hash", "producer"):
            _require_text(getattr(self, name), f"ArtifactRef.{name}")


@dataclass(frozen=True, slots=True)
class Metric:
    name: str
    value: float
    split: str
    unit: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.name, "Metric.name")
        _require_text(self.split, "Metric.split")


@dataclass(slots=True)
class Experiment:
    """The append-oriented record linking a task, strategy, artifacts, and results."""

    id: str
    task_id: str
    strategy_id: str
    hypothesis: str
    budget: Budget = field(default_factory=Budget)
    parent_experiment_id: str | None = None
    status: ExperimentStatus = ExperimentStatus.CREATED
    artifacts: list[ArtifactRef] = field(default_factory=list)
    metrics: list[Metric] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        for name in ("id", "task_id", "strategy_id", "hypothesis"):
            _require_text(getattr(self, name), f"Experiment.{name}")
        if self.completed_at is not None and self.completed_at < self.created_at:
            raise ValueError("Experiment.completed_at cannot precede created_at")

    def add_artifact(self, artifact: ArtifactRef) -> None:
        if any(existing.id == artifact.id for existing in self.artifacts):
            raise ValueError(f"Duplicate artifact id: {artifact.id}")
        self.artifacts.append(artifact)

    def add_metric(self, metric: Metric) -> None:
        self.metrics.append(metric)

    def mark_completed(self, status: ExperimentStatus) -> None:
        terminal = {
            ExperimentStatus.VERIFIED,
            ExperimentStatus.REJECTED,
            ExperimentStatus.FAILED,
            ExperimentStatus.BUDGET_EXCEEDED,
        }
        if status not in terminal:
            raise ValueError("Completed experiments require a terminal status")
        self.status = status
        self.completed_at = utc_now()

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly representation for later storage."""
        result = asdict(self)
        result["status"] = self.status.value
        result["budget"] = asdict(self.budget)
        result["artifacts"] = [
            {**asdict(artifact), "kind": artifact.kind.value}
            for artifact in self.artifacts
        ]
        return result


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
