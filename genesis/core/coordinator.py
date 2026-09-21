from __future__ import annotations

from pathlib import Path

from genesis.agents import Builder, Critic, Researcher
from genesis.evaluation import IndependentEvaluator, TASK
from genesis.providers import MockProvider
from genesis.storage import ArtifactStore, ExperimentDatabase

from .events import transition_experiment
from .models import Experiment, ExperimentStatus, Strategy


class Coordinator:
    def __init__(self, root: str | Path = ".genesis"):
        self.root = Path(root)
        self.db = ExperimentDatabase(self.root / "experiments.sqlite3")
        self.artifacts = ArtifactStore(self.root / "artifacts")
        self.provider = MockProvider()
        self.researcher = Researcher()
        self.builder = Builder()
        self.critic = Critic()
        self.evaluator = IndependentEvaluator()

    def run_once(self, experiment_id: str = "EXP-000001") -> dict[str, object]:
        strategy = Strategy("baseline-v1", "Direct baseline", "1", ("research", "build", "evaluate"))
        experiment = Experiment(
            id=experiment_id,
            task_id=TASK.id,
            strategy_id=strategy.id,
            hypothesis="A deterministic baseline establishes a reproducible reference score.",
        )
        self.db.save_experiment(experiment)

        self._transition(experiment, ExperimentStatus.RESEARCHING, "researcher")
        self.researcher.run(experiment, self.provider)
        self._transition(experiment, ExperimentStatus.BUILDING, "builder")
        artifact = self.builder.run(experiment, self.artifacts)
        experiment.add_artifact(artifact)
        self._transition(experiment, ExperimentStatus.EXECUTING, "runner")
        self._transition(experiment, ExperimentStatus.EVALUATING, "evaluator")
        evaluation = self.evaluator.evaluate(Path(artifact.path).read_text(encoding="utf-8"))
        experiment.add_metric(__import__("genesis.core", fromlist=["Metric"]).Metric("pass_rate", evaluation.score, "all"))
        self._transition(experiment, ExperimentStatus.CRITIQUING, "critic")
        critique = self.critic.run(evaluation.failures)
        experiment.metadata["evaluation"] = evaluation.as_dict()
        experiment.metadata["critique"] = critique
        self._transition(experiment, ExperimentStatus.STORED, "store")
        final_status = ExperimentStatus.VERIFIED if evaluation.score == 1.0 else ExperimentStatus.REJECTED
        self._transition(experiment, final_status, "evaluator", {"score": evaluation.score})
        self.db.save_experiment(experiment)
        return {
            "experiment": experiment.to_dict(),
            "evaluation": evaluation.as_dict(),
            "critique": critique,
        }

    def _transition(self, experiment: Experiment, target: ExperimentStatus, actor: str, payload: dict[str, object] | None = None) -> None:
        event = transition_experiment(experiment, target, actor=actor, payload=payload)
        self.db.save_experiment(experiment)
        self.db.append_event(event)
