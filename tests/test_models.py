from datetime import datetime, timezone

import pytest

from genesis.core import (
    ArtifactKind,
    ArtifactRef,
    Budget,
    Experiment,
    ExperimentStatus,
    Metric,
    Strategy,
    Task,
)


def test_task_requires_evaluation_cases():
    with pytest.raises(ValueError, match="evaluation case"):
        Task("task-1", "Example", "Solve it", "v1")


def test_strategy_rejects_empty_steps():
    with pytest.raises(ValueError, match="steps"):
        Strategy("strategy-1", "Baseline", "1", ())


def test_experiment_serializes_nested_domain_data():
    experiment = Experiment(
        id="EXP-000001",
        task_id="python-001",
        strategy_id="baseline-1",
        hypothesis="Direct generation establishes a baseline.",
        budget=Budget(max_runtime_seconds=30),
    )
    experiment.add_artifact(
        ArtifactRef("artifact-1", "solution.py", ArtifactKind.SOURCE, "abc123", "builder")
    )
    experiment.add_metric(Metric("pass_rate", 0.75, "development"))

    payload = experiment.to_dict()

    assert payload["status"] == "created"
    assert payload["budget"]["max_runtime_seconds"] == 30
    assert payload["artifacts"][0]["kind"] == "source"
    assert payload["metrics"][0]["name"] == "pass_rate"


def test_experiment_terminal_status_records_completion():
    experiment = Experiment(
        id="EXP-000002",
        task_id="python-001",
        strategy_id="baseline-1",
        hypothesis="Measure the baseline.",
    )

    experiment.mark_completed(ExperimentStatus.REJECTED)

    assert experiment.status is ExperimentStatus.REJECTED
    assert isinstance(experiment.completed_at, datetime)
    assert experiment.completed_at.tzinfo is timezone.utc


def test_experiment_rejects_duplicate_artifacts():
    experiment = Experiment("EXP-000003", "task", "strategy", "hypothesis")
    artifact = ArtifactRef("artifact-1", "solution.py", ArtifactKind.SOURCE, "hash", "builder")
    experiment.add_artifact(artifact)

    with pytest.raises(ValueError, match="Duplicate artifact"):
        experiment.add_artifact(artifact)
