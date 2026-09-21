from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class BenchmarkSplit(StrEnum):
    EXPERIENCE = "experience"
    VALIDATION = "validation"
    HIDDEN = "hidden"


@dataclass(frozen=True, slots=True)
class BenchmarkDefinition:
    id: str
    version: str
    task_family: str
    experience_cases: tuple[object, ...]
    validation_cases: tuple[object, ...]
    hidden_case_count: int

    def cases_for(self, split: BenchmarkSplit) -> tuple[object, ...]:
        if split is BenchmarkSplit.EXPERIENCE:
            return self.experience_cases
        if split is BenchmarkSplit.VALIDATION:
            return self.validation_cases
        raise ValueError("Hidden cases are never exposed through the public registry")


class BenchmarkRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, BenchmarkDefinition] = {}

    def register(self, benchmark: BenchmarkDefinition) -> None:
        if benchmark.id in self._definitions:
            raise ValueError(f"Benchmark already registered: {benchmark.id}")
        if benchmark.hidden_case_count < 1:
            raise ValueError("A benchmark must reserve hidden cases")
        self._definitions[benchmark.id] = benchmark

    def get(self, benchmark_id: str) -> BenchmarkDefinition:
        return self._definitions[benchmark_id]

    def list(self) -> tuple[BenchmarkDefinition, ...]:
        return tuple(self._definitions.values())

    def public_cases(self, benchmark_id: str) -> tuple[object, ...]:
        benchmark = self.get(benchmark_id)
        return benchmark.experience_cases + benchmark.validation_cases
