from datetime import date

from genesis.core import ExperimentIdentity
from genesis.evaluation import (
    BenchmarkDefinition,
    BenchmarkRegistry,
    BenchmarkSplit,
    LearningCurve,
    TrialMetrics,
)
from genesis.evidence import EvidenceGraph, EvidenceSource
from genesis.evolution import ImprovementLoop
from genesis.memory import StrategyMemory, StrategyMemoryEntry
from genesis.planning import DynamicPlanner
from genesis.safety import KillSwitch, PolicyEngine
from genesis.skills import SkillContract, default_registry


def test_identity_is_stable_and_includes_all_runtime_dimensions():
    first = ExperimentIdentity("0.1.3", "mock-v1", "skills-v1", "workflow-v1", "policy-v1", ("python",), "linux", 7)
    second = ExperimentIdentity("0.1.3", "mock-v1", "skills-v1", "workflow-v1", "policy-v1", ("python",), "linux", 7)
    assert first.fingerprint() == second.fingerprint()
    assert "fingerprint" in first.as_dict()


def test_benchmark_registry_does_not_expose_hidden_cases():
    registry = BenchmarkRegistry()
    registry.register(BenchmarkDefinition("demo", "1", "reasoning", (1,), (2,), 1))
    assert registry.get("demo").cases_for(BenchmarkSplit.EXPERIENCE) == (1,)
    try:
        registry.get("demo").cases_for(BenchmarkSplit.HIDDEN)
    except ValueError:
        pass
    else:
        raise AssertionError("hidden cases must stay private")


def test_memory_and_dynamic_planner_reuse_failure_lessons(tmp_path):
    memory = StrategyMemory(tmp_path / "memory.json")
    memory.record(StrategyMemoryEntry("task-x", "s1", "rejected", 0.2, "Do not skip source verification."))
    plan = DynamicPlanner(default_registry(), memory).plan("task-x", "research and verify a claim")
    assert "verification" in plan.skill_ids
    assert "apply_recalled_lessons" in plan.steps


def test_evidence_graph_reports_contested_claims():
    graph = EvidenceGraph()
    graph.add("claim", EvidenceSource("a", "https://a", 0.9, date(2026, 1, 1), True))
    graph.add("claim", EvidenceSource("b", "https://b", 0.8, date(2026, 1, 2), False))
    result = graph.assess("claim")
    assert result.status == "contested"
    assert 0.5 < result.confidence < 0.6


def test_learning_curve_prefers_quality_with_cost_and_safety():
    curve = LearningCurve()
    baseline = TrialMetrics(1, 0.6, True, 100, 0.1, 2)
    candidate = TrialMetrics(2, 0.8, True, 100, 0.1, 2)
    curve.add(baseline)
    curve.add(candidate)
    assert curve.compare(baseline, candidate)
    assert curve.best() == candidate


def test_contract_policy_and_external_kill_switch(tmp_path):
    contract = SkillContract("Task", "Result", permissions=("filesystem:project",), risk_level="medium")
    assert contract.timeout_seconds == 30
    decision = PolicyEngine().decide("write-file", "medium", {"filesystem:project"}, {"filesystem:project"})
    assert decision.allowed and decision.requires_approval
    switch = KillSwitch(tmp_path / "STOP")
    switch.stop()
    assert switch.is_stopped()


def test_improvement_loop_records_rejection_and_acceptance(tmp_path):
    memory = StrategyMemory(tmp_path / "memory.json")
    loop = ImprovementLoop(memory)
    baseline = TrialMetrics(1, 0.6, True, 100, 0.1, 2)
    rejected = loop.compare("task", baseline, TrialMetrics(2, 0.5, True, 100, 0.1, 2), "quality regressed")
    accepted = loop.compare("task", baseline, TrialMetrics(3, 0.8, True, 100, 0.1, 2), "quality improved")
    assert not rejected.accepted
    assert accepted.accepted
    assert len(memory.recall("task")) == 2
