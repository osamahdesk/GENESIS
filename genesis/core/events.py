"""Domain events and the experiment lifecycle state machine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .models import Experiment, ExperimentStatus, utc_now

_ALLOWED_TRANSITIONS: dict[ExperimentStatus, frozenset[ExperimentStatus]] = {
    ExperimentStatus.CREATED: frozenset({ExperimentStatus.RESEARCHING, ExperimentStatus.FAILED}),
    ExperimentStatus.RESEARCHING: frozenset({ExperimentStatus.BUILDING, ExperimentStatus.FAILED}),
    ExperimentStatus.BUILDING: frozenset({ExperimentStatus.EXECUTING, ExperimentStatus.FAILED}),
    ExperimentStatus.EXECUTING: frozenset({ExperimentStatus.EVALUATING, ExperimentStatus.FAILED, ExperimentStatus.BUDGET_EXCEEDED}),
    ExperimentStatus.EVALUATING: frozenset({ExperimentStatus.CRITIQUING, ExperimentStatus.STORED, ExperimentStatus.FAILED}),
    ExperimentStatus.CRITIQUING: frozenset({ExperimentStatus.STORED, ExperimentStatus.FAILED}),
    ExperimentStatus.STORED: frozenset({ExperimentStatus.VERIFIED, ExperimentStatus.REJECTED}),
    ExperimentStatus.VERIFIED: frozenset(),
    ExperimentStatus.REJECTED: frozenset(),
    ExperimentStatus.FAILED: frozenset(),
    ExperimentStatus.BUDGET_EXCEEDED: frozenset(),
}


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """An append-only record of a significant domain action."""

    name: str
    experiment_id: str
    actor: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=utc_now)
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("DomainEvent.name must be non-empty")
        if not self.experiment_id.strip():
            raise ValueError("DomainEvent.experiment_id must be non-empty")
        if not self.actor.strip():
            raise ValueError("DomainEvent.actor must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "experiment_id": self.experiment_id,
            "actor": self.actor,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "schema_version": self.schema_version,
        }


def allowed_transitions(status: ExperimentStatus) -> frozenset[ExperimentStatus]:
    return _ALLOWED_TRANSITIONS[status]


def transition_experiment(
    experiment: Experiment,
    target: ExperimentStatus,
    *,
    actor: str,
    payload: dict[str, Any] | None = None,
) -> DomainEvent:
    """Move an experiment through an allowed transition and return its event."""
    if target not in allowed_transitions(experiment.status):
        raise ValueError(f"Invalid experiment transition: {experiment.status} -> {target}")

    previous = experiment.status
    experiment.status = target
    if target in {
        ExperimentStatus.VERIFIED,
        ExperimentStatus.REJECTED,
        ExperimentStatus.FAILED,
        ExperimentStatus.BUDGET_EXCEEDED,
    }:
        experiment.completed_at = utc_now()

    return DomainEvent(
        name="experiment.status_changed",
        experiment_id=experiment.id,
        actor=actor,
        payload={
            "from": previous.value,
            "to": target.value,
            **(payload or {}),
        },
    )
