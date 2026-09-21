import pytest

from genesis.core import DomainEvent, Experiment, ExperimentStatus, transition_experiment


def make_experiment() -> Experiment:
    return Experiment("EXP-000010", "task", "strategy", "hypothesis")


def test_valid_lifecycle_transition_creates_event():
    experiment = make_experiment()

    event = transition_experiment(experiment, ExperimentStatus.RESEARCHING, actor="coordinator")

    assert experiment.status is ExperimentStatus.RESEARCHING
    assert event.name == "experiment.status_changed"
    assert event.payload == {"from": "created", "to": "researching"}
    assert event.to_dict()["timestamp"]


def test_invalid_transition_is_rejected():
    experiment = make_experiment()

    with pytest.raises(ValueError, match="Invalid experiment transition"):
        transition_experiment(experiment, ExperimentStatus.VERIFIED, actor="coordinator")


def test_terminal_transition_records_completion_time():
    experiment = make_experiment()
    transition_experiment(experiment, ExperimentStatus.RESEARCHING, actor="coordinator")
    transition_experiment(experiment, ExperimentStatus.BUILDING, actor="coordinator")
    transition_experiment(experiment, ExperimentStatus.EXECUTING, actor="coordinator")
    transition_experiment(experiment, ExperimentStatus.EVALUATING, actor="evaluator")
    transition_experiment(experiment, ExperimentStatus.STORED, actor="store")

    event = transition_experiment(
        experiment,
        ExperimentStatus.VERIFIED,
        actor="evaluator",
        payload={"score": 0.8},
    )

    assert experiment.completed_at is not None
    assert event.payload["score"] == 0.8


def test_event_requires_identity_fields():
    with pytest.raises(ValueError, match="actor"):
        DomainEvent("experiment.created", "EXP-1", "")
