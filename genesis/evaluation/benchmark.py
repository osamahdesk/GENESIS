from __future__ import annotations

from dataclasses import dataclass

from genesis.core import Task


@dataclass(frozen=True, slots=True)
class Case:
    value: int
    expected: int
    split: str


TASK = Task(
    id="python-sum-squares-v1",
    name="Sum squares",
    statement="Read a JSON integer n from stdin and print the sum of squares from 1 through n as JSON.",
    benchmark_version="python-sum-squares-v1",
    development_cases=("1", "3"),
    validation_cases=("5", "10"),
    hidden_cases=("0", "7", "12"),
)

CASES = (
    Case(1, 1, "development"),
    Case(3, 14, "development"),
    Case(5, 55, "validation"),
    Case(10, 385, "validation"),
    Case(0, 0, "hidden"),
    Case(7, 140, "hidden"),
    Case(12, 650, "hidden"),
)
