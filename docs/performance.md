# GENESIS Performance Engineering

## Principle

GENESIS treats speed as a measured property, not a slogan. Every optimization must preserve score, evidence, lifecycle events, and the selected safety boundary.

## Optimizations

The evaluator now supports three useful paths. Isolated mode starts a fresh interpreter for every case and provides the strongest separation. Batch mode starts one isolated worker for a benchmark group and creates a fresh namespace and redirected standard input/output for each case. Cache mode reuses an evaluation only when the source, cases, and execution mode hash match exactly.

The local Hugging Face provider also keeps the model in evaluation mode and uses `torch.inference_mode()` with key/value caching for generation.

## Measured result

The included benchmark uses the seven-case sum-of-squares task on the same machine and records wall time with Python's monotonic clock:

| Path | Wall time | Result |
|---|---:|---|
| Per-case isolated evaluation | 0.327261 s | 7/7, score 1.0 |
| Accelerated batch evaluation | 0.047891 s | 7/7, score 1.0 |
| In-memory repeated evaluation | 0.000051 s | Cache hit, score 1.0 |

The measured batch improvement in this run was **6.83×** over isolated evaluation. The repeated in-memory lookup was approximately **939×** faster than the cold batch evaluation. These numbers are benchmark-specific and must not be generalized to every model, task, machine, or workload.

The benchmark commands are:

```bash
python tools/benchmark_speed.py
python tools/benchmark_cli_cache.py
```

The CLI benchmark confirms that process startup, database writes, artifact hashing, and JSON output remain part of end-to-end latency. Therefore a component can be hundreds of times faster while the whole command is only modestly faster. This distinction prevents misleading performance claims.

## Safety trade-off

Batch mode is intended for controlled benchmark artifacts. Per-case isolated mode remains available through `IndependentEvaluator(accelerated=False)` when the artifact is hostile or maximum process separation is required. No optimization is allowed to disable the evaluator, bypass hidden cases, or grant host access.
