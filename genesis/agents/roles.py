from __future__ import annotations

from dataclasses import dataclass

from genesis.core import ArtifactKind, ArtifactRef, Experiment
from genesis.providers import ModelProvider
from genesis.storage import ArtifactStore


@dataclass(frozen=True, slots=True)
class ResearchOutput:
    hypothesis: str
    strategy_steps: tuple[str, ...]


class Researcher:
    name = "researcher"

    def run(self, experiment: Experiment, provider: ModelProvider) -> ResearchOutput:
        provider.generate(experiment.hypothesis)
        return ResearchOutput(
            hypothesis=experiment.hypothesis,
            strategy_steps=("read_task", "generate_solution", "return_json"),
        )


class Builder:
    name = "builder"

    def run(self, experiment: Experiment, artifact_store: ArtifactStore) -> ArtifactRef:
        # The first offline benchmark has a deterministic baseline artifact. The
        # provider boundary remains ready for a model-backed builder later.
        source = (
            "import json\n\n"
            "n = int(json.load(__import__('sys').stdin))\n"
            "print(json.dumps(n * (n + 1) * (2 * n + 1) // 6))\n"
        )
        return artifact_store.put_text(
            f"{experiment.id}-solution",
            f"{experiment.id}/solution.py",
            source,
            ArtifactKind.SOURCE,
            self.name,
        )


class Critic:
    name = "critic"

    def run(self, failures: list[str]) -> dict[str, object]:
        return {
            "failure_count": len(failures),
            "summary": "No failures detected." if not failures else "Inspect failed benchmark cases.",
        }
