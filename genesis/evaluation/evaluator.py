from __future__ import annotations

import json
from dataclasses import dataclass

from genesis.environment import RestrictedRunner

from .benchmark import CASES, Case


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    score: float
    passed: int
    total: int
    split_scores: dict[str, float]
    failures: list[str]
    runtime_ms: int

    def as_dict(self) -> dict[str, object]:
        return {
            "score": self.score,
            "passed": self.passed,
            "total": self.total,
            "split_scores": self.split_scores,
            "failures": self.failures,
            "runtime_ms": self.runtime_ms,
        }


class IndependentEvaluator:
    def __init__(self, runner: RestrictedRunner | None = None):
        self.runner = runner or RestrictedRunner()

    def evaluate(self, source: str, cases: tuple[Case, ...] = CASES) -> EvaluationResult:
        passed = 0
        failures: list[str] = []
        split_totals: dict[str, list[int]] = {}
        runtime = 0
        for case in cases:
            result = self.runner.run(source, json.dumps(case.value))
            runtime += result.runtime_ms
            actual = None
            if not result.timed_out and result.returncode == 0:
                try:
                    actual = json.loads(result.stdout.strip())
                except json.JSONDecodeError:
                    actual = None
            ok = actual == case.expected
            split_totals.setdefault(case.split, [0, 0])[1] += 1
            if ok:
                passed += 1
                split_totals[case.split][0] += 1
            else:
                failures.append(f"{case.split}:{case.value}: expected {case.expected}, got {actual}")
        split_scores = {key: good / total for key, (good, total) in split_totals.items()}
        return EvaluationResult(passed / len(cases), passed, len(cases), split_scores, failures, runtime)
