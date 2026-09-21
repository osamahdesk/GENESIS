# GENESIS Next Architecture

GENESIS is evolving around one auditable loop:

```text
Capability → Experiment → Evaluation → Learning → Re-experiment
```

The new foundations are deliberately small and composable. `ExperimentIdentity` records the GENESIS, model, skills, workflow, policy, tools, environment, and seed versions. Its fingerprint prevents comparisons that silently mix incompatible runtime conditions.

`BenchmarkRegistry` separates experience and validation cases from a reserved hidden split. Public planning can use experience and validation data, but hidden cases are not returned by the registry. This prevents the optimization loop from treating the final test as training data.

`SkillContract` gives every capability the same contract: input, output, preconditions, permissions, risk, cost, timeout, evaluation, and rollback. `SkillRegistry` and `DynamicPlanner` select a minimal explainable plan for a task instead of assuming that every task needs the same fixed workflow.

`StrategyMemory` stores both successful and failed outcomes as lessons. A failure is not discarded: its fingerprint, strategy, score, and lesson remain available to a later plan. The memory is retrieval, not proof; every claimed improvement still requires an independent evaluation.

`EvidenceGraph` represents claims, sources, reliability, support, contradiction, and confidence. A contested claim remains contested rather than being flattened into an unsupported answer.

`PolicyEngine` centralizes risk decisions, while `KillSwitch` exists outside the agent process. A high-risk action cannot be approved merely because a model requested it, and a stopped switch interrupts future execution regardless of the agent's internal state.

`LearningCurve` records quality, runtime, estimated cost, tool calls, and safety violations. A candidate must improve utility without increasing safety violations before it can pass a regression gate. The goal is a reproducible learning curve, not a single impressive demo.

The current release contains the first tested foundations and integrates the identity, plan, and strategy memory into the Coordinator. External browser, terminal, cloud, and write-capable tools remain separate milestones until their contracts and isolation boundaries are implemented.
