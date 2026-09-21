import time

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
