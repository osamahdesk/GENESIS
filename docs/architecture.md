# GENESIS Architecture

## Architectural principle

The system separates proposal, execution, evaluation, and evidence. No agent is allowed to be the sole authority over the result it helped produce.

```text
CLI
 ↓
Coordinator
 ├── Provider adapter
 ├── Researcher
 ├── Builder
 ├── Restricted runner
 ├── Independent evaluator
 ├── Critic
 └── Experiment store
```

## Core contracts

### Task

A task defines the problem, input/output contract, benchmark version, visible data policy, and evaluation policy. A task is immutable after an experiment begins.

### Strategy

A strategy is a versioned workflow description. In v0.1 it may contain role order, prompt-template references, retry policy, and evaluation settings. It is data, not executable authority.

### Artifact

An artifact is a generated file or bundle with a content hash, media type, producer role, parent experiment, and validation status. The runner receives a copy, never the source store itself.

### Experiment

An experiment is the primary unit of work. It links a task, strategy, agents, artifacts, events, evaluations, failures, and decision. The record is append-oriented: new attempts and evaluations are added rather than replacing history.

### Evaluation

An evaluation contains benchmark identity, test split, metric values, test outcomes, runtime, resource usage, and evaluator version. It must be independently reproducible from the recorded inputs.

## Coordinator responsibilities

The Coordinator creates an experiment, enforces the state machine, allocates budgets, invokes roles, records events, handles retries, and stops on terminal states. It does not reinterpret scores or convert an agent opinion into a verified result.

## Event model

Important actions produce structured events such as `experiment.created`, `agent.started`, `artifact.created`, `evaluation.completed`, `experiment.failed`, and `decision.recorded`. Events contain a timestamp, run identifier, experiment identifier, actor, payload, and schema version.

## Storage choice

v0.1 uses SQLite for indexed metadata and a filesystem artifact store for large files. The database stores hashes and references; it does not need to contain every log or generated file as a large text blob.

## Reproducibility identity

A run identity includes the Git commit, configuration hash, prompt bundle hash, benchmark hash, model identifier and parameters, Python version, dependency lock information, operating-system metadata, and random seed when applicable.

## Extension boundaries

Future components such as strategy evolution, external research, and tool discovery must implement interfaces above the Coordinator. They may propose candidates, but promotion remains behind the same evaluation and regression gates.
