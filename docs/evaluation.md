# GENESIS Evaluation Protocol

## Purpose

The evaluation system answers one question: did a candidate workflow perform better under fair and independently measured conditions?

## Controlled comparison

A baseline and candidate must use the same task set, model, model parameters, token and time budgets, environment policy, retry policy, and reporting format. Any difference is recorded as an experimental variable.

## Baselines

The first benchmark should compare at least these workflows:

1. Single model produces a solution directly.
2. Single model produces a solution and performs self-critique.
3. Researcher → Builder → Evaluator.
4. Researcher → Builder → Critic → Repair → Evaluator.

The purpose is attribution. A larger workflow must not be called better merely because it used more model calls.

## Splits

- **Development:** visible during workflow design.
- **Validation:** used for candidate selection without being used to write task-specific answers.
- **Hidden:** held outside the agent workspace and used only by the independent evaluator.
- **Unseen:** a later task collection used to test generalization.

The repository may publish hashes and protocols for hidden data without publishing the hidden cases.

## Repeated trials

A single run is evidence of behavior, not proof of improvement. Strategy comparisons should support at least three independent trials and preferably five or more when model randomness is material. Reports include mean, median, spread, best, worst, and per-task results.

## Metrics

Correctness is primary for the first Python benchmark. Additional metrics are recorded separately:

```text
correctness / pass rate
hidden-task performance
latency
model calls
input and output tokens
estimated cost
memory and disk usage
retry count
failure rate
```

A candidate is not automatically accepted when correctness rises but reliability, cost, latency, or hidden-task performance regresses severely.

## Ablation plan

The first research report should compare the contribution of memory, critic, repair, and strategy mutation. Remove one component at a time while keeping the rest of the conditions fixed.

## Decision policy

A candidate is `SUPPORTED` when it improves the primary metric in the recorded comparison. It is `REPLICATED` when the improvement appears across independent trials. It is `VERIFIED` only when it also passes hidden or unseen evaluation and the configured regression gate.

## Failure reporting

A negative result is valid output. Reports must preserve failures, budget exhaustion, timeouts, rejected candidates, and cases where an apparent visible-set improvement disappears on hidden tasks.
