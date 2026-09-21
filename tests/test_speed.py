
from genesis.evaluation import CASES, IndependentEvaluator

SOURCE = "import json\nn = int(json.load(__import__('sys').stdin))\nprint(json.dumps(n * (n + 1) * (2 * n + 1) // 6))\n"


def test_accelerated_evaluation_preserves_correctness():
    fast = IndependentEvaluator(accelerated=True).evaluate(SOURCE, CASES)
    safe = IndependentEvaluator(accelerated=False).evaluate(SOURCE, CASES)

    assert fast.score == safe.score == 1.0
    assert fast.passed == safe.passed == len(CASES)
    assert fast.execution_mode == "batch"
    assert safe.execution_mode == "isolated"


def test_evaluator_cache_returns_zero_work_runtime_on_repeat():
    evaluator = IndependentEvaluator(accelerated=True)
    evaluator.evaluate(SOURCE, CASES)
    cached = evaluator.evaluate(SOURCE, CASES)

    assert cached.cache_hit is True
    assert cached.runtime_ms == 0


class BrokenBatchRunner:
    def run_batch(self, source, inputs):
        from genesis.environment import RunResult

        return [RunResult(1, "", "batch unavailable", False, 1) for _ in inputs]

    def run(self, source, stdin=""):
        from genesis.environment import RunResult

        value = int(stdin)
        return RunResult(0, str(value * value) + "\n", "", False, 1)


def test_mobile_fallback_uses_isolated_runner_when_batch_has_no_output():
    from genesis.evaluation import Case

    cases = (Case(2, 4, "development"),)
    evaluator = IndependentEvaluator(runner=BrokenBatchRunner(), accelerated=True)
    result = evaluator.evaluate("ignored", cases)

    assert result.score == 1.0
    assert result.execution_mode == "batch-fallback-isolated"
