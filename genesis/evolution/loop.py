from __future__ import annotations

from dataclasses import dataclass

from genesis.evaluation import LearningCurve, TrialMetrics
from genesis.memory import StrategyMemory, StrategyMemoryEntry


@dataclass(frozen=True, slots=True)
class ImprovementDecision:
    accepted: bool
    reason: str
    baseline_utility: float
    candidate_utility: float


class ImprovementLoop:
    """Promote only candidates that beat baseline utility without new safety violations."""

    def __init__(self, memory: StrategyMemory | None = None) -> None:
        self.memory = memory or StrategyMemory()
        self.curve = LearningCurve()

    def compare(self, task_signature: str, baseline: TrialMetrics, candidate: TrialMetrics, lesson: str) -> ImprovementDecision:
        self.curve.add(baseline)
        self.curve.add(candidate)
        accepted = self.curve.compare(baseline, candidate)
        reason = "candidate beats baseline without additional safety violations" if accepted else "candidate rejected by regression gate"
        self.memory.record(
            StrategyMemoryEntry(
                task_signature,
                f"candidate-{candidate.experiment_number}",
                "accepted" if accepted else "rejected",
                candidate.quality,
                lesson,
                "" if accepted else reason,
            )
        )
        return ImprovementDecision(accepted, reason, baseline.utility(), candidate.utility())
