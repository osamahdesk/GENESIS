from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

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
    execution_mode: str = "batch"
    cache_hit: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "score": self.score,
            "passed": self.passed,
            "total": self.total,
            "split_scores": self.split_scores,
            "failures": self.failures,
            "runtime_ms": self.runtime_ms,
            "execution_mode": self.execution_mode,
            "cache_hit": self.cache_hit,
        }


class IndependentEvaluator:
    def __init__(self, runner: RestrictedRunner | None = None, accelerated: bool = True, cache_dir: str | Path | None = None):
        self.runner = runner or RestrictedRunner()
        self.accelerated = accelerated
        self._cache: dict[str, EvaluationResult] = {}
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def evaluate(self, source: str, cases: tuple[Case, ...] = CASES) -> EvaluationResult:
        key = hashlib.sha256((source + repr(cases) + str(self.accelerated)).encode()).hexdigest()
        cached = self._cache.get(key) or self._load_persistent(key)
        if cached:
            return EvaluationResult(cached.score, cached.passed, cached.total, cached.split_scores, cached.failures, 0, cached.execution_mode, True)
        inputs = [json.dumps(case.value) for case in cases]
        execution_mode = "isolated"
        if self.accelerated:
            results = self.runner.run_batch(source, inputs)
            # Some mobile Python builds restrict runpy/subprocess behavior. If
            # the accelerated worker cannot produce a parseable case, retry
            # with the portable per-case runner instead of rejecting the task.
            batch_has_output = len(results) == len(inputs) and all(
                result.returncode == 0 and not result.timed_out and result.stdout.strip()
                for result in results
            )
            if not batch_has_output:
                results = [self.runner.run(source, value) for value in inputs]
                execution_mode = "batch-fallback-isolated"
            else:
                execution_mode = "batch"
        else:
            results = [self.runner.run(source, value) for value in inputs]
        passed = 0
        failures: list[str] = []
        split_totals: dict[str, list[int]] = {}
        runtime = 0
        for case, result in zip(cases, results, strict=True):
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
        result = EvaluationResult(passed / len(cases), passed, len(cases), split_scores, failures, runtime, execution_mode)
        self._cache[key] = result
        self._save_persistent(key, result)
        return result

    def _load_persistent(self, key: str) -> EvaluationResult | None:
        if not self.cache_dir:
            return None
        path = self.cache_dir / f"{key}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return EvaluationResult(data["score"], data["passed"], data["total"], data["split_scores"], data["failures"], data["runtime_ms"], data["execution_mode"], False)

    def _save_persistent(self, key: str, result: EvaluationResult) -> None:
        if self.cache_dir:
            (self.cache_dir / f"{key}.json").write_text(json.dumps(result.as_dict(), indent=2) + "\n", encoding="utf-8")
