from __future__ import annotations

import json
import tempfile
import time
from pathlib import Path

from genesis.evaluation import CASES, IndependentEvaluator


def main() -> None:
    source = "import json\nn = int(json.load(__import__('sys').stdin))\nprint(json.dumps(n * (n + 1) * (2 * n + 1) // 6))\n"
    results = {}
    for label, accelerated in (("isolated", False), ("batch", True)):
        evaluator = IndependentEvaluator(accelerated=accelerated)
        started = time.perf_counter()
        result = evaluator.evaluate(source, CASES)
        elapsed = time.perf_counter() - started
        started_cached = time.perf_counter()
        cached = evaluator.evaluate(source, CASES)
        cached_elapsed = time.perf_counter() - started_cached
        results[label] = {
            "wall_seconds": round(elapsed, 6),
            "reported_runtime_ms": result.runtime_ms,
            "score": result.score,
            "passed": result.passed,
            "cache_wall_seconds": round(cached_elapsed, 6),
            "cache_hit": cached.cache_hit,
        }
    results["speedup_batch_vs_isolated"] = round(results["isolated"]["wall_seconds"] / results["batch"]["wall_seconds"], 2)
    results["speedup_cache_vs_batch"] = round(results["batch"]["wall_seconds"] / max(results["batch"]["cache_wall_seconds"], 1e-9), 2)
    output = Path(tempfile.gettempdir()) / "genesis-speed-benchmark.json"
    output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(output)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
