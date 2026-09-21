# GENESIS Work Tree

```text
GENESIS
├── 0. Project contract
│   ├── Vision and research question
│   ├── Scope boundaries
│   ├── Definitions and evidence hierarchy
│   └── Release acceptance criteria
│
├── 1. Foundation
│   ├── Python package and CLI entry point
│   ├── Configuration loading and validation
│   ├── Typed schemas
│   ├── Event and logging model
│   └── Offline mock provider
│
├── 2. Experiment core
│   ├── Task definition
│   ├── Strategy definition
│   ├── Experiment lifecycle
│   ├── Budget model
│   ├── Artifact references and hashes
│   └── Coordinator
│
├── 3. Agent roles
│   ├── Agent interface
│   ├── Researcher
│   ├── Builder
│   └── Critic / failure analyst
│
├── 4. Execution and evaluation
│   ├── Restricted runner
│   ├── Benchmark loader
│   ├── Visible evaluation
│   ├── Validation evaluation
│   ├── Hidden evaluation
│   └── Regression and anti-cheating checks
│
├── 5. Evidence and memory
│   ├── SQLite experiment store
│   ├── Reproducibility bundle
│   ├── Failure memory
│   ├── Verified knowledge
│   └── Provenance and status transitions
│
├── 6. Scientific comparison
│   ├── Frozen baseline
│   ├── Repeated trials
│   ├── Cost and resource metrics
│   ├── Ablation reports
│   └── Generalization evaluation
│
├── 7. Strategy evolution
│   ├── Mutation operators
│   ├── Candidate population
│   ├── Selection policy
│   ├── Lineage graph
│   └── Regression gate
│
├── 8. Future research
│   ├── Dynamic roles
│   ├── Tool registry and tool experiments
│   ├── Capability frontier
│   ├── Knowledge graph
│   └── Controlled external research
│
└── 9. Release and community
    ├── Documentation
    ├── Tests and security review
    ├── Example experiment
    ├── Changelog and versioning
    └── Contribution workflow
```

## Dependency order

The dependency direction is strict:

```text
Schemas → Events → Storage → Runner/Evaluator → Agents → Coordinator → CLI → Evolution
```

External research and dynamic self-improvement depend on a stable evaluator, a stable security boundary, and reproducible experiment records.
