# GENESIS Security Model

## Default posture

GENESIS is deny-by-default. Generated artifacts receive only the permissions required by the current experiment. Network access is off unless a future experiment explicitly enables read-only access. Credentials, host files, evaluator files, and the source repository are outside the artifact workspace.

## Execution modes

The project distinguishes three modes:

- `offline-mock`: no external model or network; used by tests.
- `restricted-local`: local subprocess limits with documented operating-system limitations.
- `container-isolated`: stronger isolation when a supported container runtime is available.

The default public example should run in offline-mock mode. Users must opt into model and execution permissions explicitly.

## Required controls

The runner must validate paths, prevent workspace escape, use timeouts, limit retries, clean temporary data, capture stdout and stderr, classify exit failures, and refuse to pass evaluator paths or secrets into generated code. Network policy and filesystem policy are recorded in every experiment.

These controls reduce risk; they do not constitute a perfect security boundary. Users must not run untrusted generated code with permissions they would not grant to an unknown program.

## Frozen infrastructure

The evaluator, hidden-test location, approval policy, experiment history, and safety configuration are frozen relative to ordinary strategy evolution. A future candidate may propose changes, but it cannot silently replace these controls.

## External-world future policy

Read-only web access, if added later, is treated as untrusted input. Web content cannot override system policy, request secrets, install software, or authorize external actions. Any write, account, financial, deletion, private-data, or public-post action requires a separate policy boundary and human approval.

## Security testing

The test suite must include workspace escape attempts, symlink cases, environment-variable leakage checks, timeout cases, subprocess behavior, network denial, malformed artifacts, and prompt-injection-like untrusted text. Known limitations are documented rather than hidden.
