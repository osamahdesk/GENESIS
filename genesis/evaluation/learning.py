from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrialMetrics:
    experiment_number: int
    quality: float
    success: bool
    runtime_ms: int
    estimated_cost: float
    tool_calls: int
    safety_violations: int = 0

    def utility(self) -> float:
        penalty = (self.runtime_ms / 100_000) + self.estimated_cost + (self.tool_calls / 1_000) + self.safety_violations
        return self.quality - penalty


@dataclass(frozen=True, slots=True)
class LearningCurvePoint:
    experiment_number: int
    quality: float
    utility: float


class LearningCurve:
    def __init__(self) -> None:
        self.trials: list[TrialMetrics] = []

    def add(self, trial: TrialMetrics) -> None:
        if trial.experiment_number <= 0:
            raise ValueError("experiment_number must be positive")
        self.trials.append(trial)

    def points(self) -> tuple[LearningCurvePoint, ...]:
        return tuple(LearningCurvePoint(t.experiment_number, t.quality, t.utility()) for t in self.trials)

    def best(self) -> TrialMetrics | None:
        return max(self.trials, key=TrialMetrics.utility, default=None)

    def compare(self, baseline: TrialMetrics, candidate: TrialMetrics) -> bool:
        return candidate.utility() > baseline.utility() and candidate.safety_violations <= baseline.safety_violations
