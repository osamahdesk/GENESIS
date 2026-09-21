from __future__ import annotations

from pathlib import Path

from genesis import __version__
from genesis.agents import Builder, Critic, Researcher
from genesis.evaluation import TASK, IndependentEvaluator
from genesis.memory import StrategyMemory, StrategyMemoryEntry
from genesis.planning import DynamicPlanner
from genesis.providers import MockProvider
from genesis.skills import default_registry
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
        self.evaluator = IndependentEvaluator(cache_dir=self.root / "evaluation-cache")
        self.memory = StrategyMemory(self.root / "strategy-memory.json")
        self.planner = DynamicPlanner(default_registry(), self.memory)

    def run_once(self, experiment_id: str = "EXP-000001") -> dict[str, object]:
        plan = self.planner.plan(TASK.id, TASK.statement)
        strategy = Strategy("baseline-v1", "Direct baseline", "1", plan.steps)
        experiment = Experiment(
            id=experiment_id,
            task_id=TASK.id,
            strategy_id=strategy.id,
            hypothesis="A deterministic baseline establishes a reproducible reference score.",
        )
        from .identity import ExperimentIdentity

        identity = ExperimentIdentity(__version__, "mock:deterministic-placeholder", "skills:v1", "planner:v1", "policy:v1", ("python-runner",), "local", 0)
        experiment.metadata["identity"] = identity.as_dict()
        experiment.metadata["plan"] = {
            "skills": plan.skill_ids,
            "steps": plan.steps,
            "recalled_lessons": plan.recalled_lessons,
        }
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
        self.memory.record(StrategyMemoryEntry(TASK.id, strategy.id, "verified" if evaluation.score == 1.0 else "rejected", evaluation.score, critique["summary"], "|".join(evaluation.failures)))
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
