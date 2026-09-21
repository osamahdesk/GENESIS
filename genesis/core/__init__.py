"""Core experiment schemas and orchestration."""

from .models import (
    ArtifactKind,
    ArtifactRef,
    Budget,
    Experiment,
    ExperimentStatus,
    Metric,
    Strategy,
    Task,
)
from .events import DomainEvent, allowed_transitions, transition_experiment
from .permissions import PermissionPolicy

__all__ = [
    "ArtifactKind",
    "ArtifactRef",
    "Budget",
    "Coordinator",
    "DomainEvent",
    "Experiment",
    "ExperimentStatus",
    "Metric",
    "PermissionPolicy",
    "Strategy",
    "Task",
    "allowed_transitions",
    "transition_experiment",
]


def __getattr__(name: str):
    if name == "Coordinator":
        from .coordinator import Coordinator

        return Coordinator
    raise AttributeError(name)
