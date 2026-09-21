from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RunResult:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool
    runtime_ms: int


class RestrictedRunner:
    """Bounded runner with secure per-case mode and accelerated batch mode.

    Batch mode keeps one isolated worker process for a group of cases. It is
    substantially faster for trusted benchmark artifacts, while per-case mode
    remains available when maximum isolation is preferred.
    """

    def __init__(self, timeout_seconds: int = 10):
        self.timeout_seconds = timeout_seconds

    def run(self, source: str, stdin: str = "") -> RunResult:
        return self._run_process(source, stdin)

    def run_batch(self, source: str, inputs: list[str]) -> list[RunResult]:
        """Run many cases in one isolated worker process.

        Each case receives a fresh namespace and redirected stdin/stdout. This
        avoids repeated interpreter startup while keeping the worker separate
        from the host process. Use per-case mode for hostile or untrusted code.
        """
        harness = '''import contextlib, io, json, runpy, sys, time\nsource_path, cases_path = sys.argv[1], sys.argv[2]\ncases = json.loads(open(cases_path, encoding="utf-8").read())\nresults = []\nfor value in cases:\n    out, err = io.StringIO(), io.StringIO()\n    old_stdin = sys.stdin\n    started = time.monotonic()\n    try:\n        sys.stdin = io.StringIO(value)\n        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):\n            runpy.run_path(source_path, run_name="__main__")\n        results.append({"returncode": 0, "stdout": out.getvalue(), "stderr": err.getvalue(), "timed_out": False, "runtime_ms": int((time.monotonic()-started)*1000)})\n    except BaseException as error:\n        results.append({"returncode": 1, "stdout": out.getvalue(), "stderr": str(error), "timed_out": False, "runtime_ms": int((time.monotonic()-started)*1000)})\n    finally:\n        sys.stdin = old_stdin\nprint(json.dumps(results))\n'''
        with tempfile.TemporaryDirectory(prefix="genesis-batch-") as directory:
            root = Path(directory)
            source_path = root / "solution.py"
            cases_path = root / "cases.json"
            harness_path = root / "harness.py"
            source_path.write_text(source, encoding="utf-8")
            cases_path.write_text(json.dumps(inputs), encoding="utf-8")
            harness_path.write_text(harness, encoding="utf-8")
            started = time.monotonic()
            try:
                completed = subprocess.run(
                    [sys.executable, "-I", str(harness_path), str(source_path), str(cases_path)],
                    capture_output=True,
                    text=True,
                    cwd=directory,
                    env={"PATH": os.environ.get("PATH", ""), "PYTHONNOUSERSITE": "1"},
                    timeout=self.timeout_seconds * max(1, len(inputs)),
                    check=False,
                )
                if completed.returncode != 0:
                    return [RunResult(completed.returncode, "", completed.stderr, False, int((time.monotonic()-started)*1000)) for _ in inputs]
                payload = json.loads(completed.stdout.strip())
                return [RunResult(item["returncode"], item["stdout"], item["stderr"], item["timed_out"], item["runtime_ms"]) for item in payload]
            except subprocess.TimeoutExpired:
                return [RunResult(-1, "", "batch timeout", True, int((time.monotonic()-started)*1000)) for _ in inputs]

    def _run_process(self, source: str, stdin: str) -> RunResult:
        with tempfile.TemporaryDirectory(prefix="genesis-run-") as directory:
            path = Path(directory) / "solution.py"
            path.write_text(source, encoding="utf-8")
            timer = time.monotonic()
            try:
                completed = subprocess.run(
                    [sys.executable, "-I", str(path)],
                    input=stdin,
                    capture_output=True,
                    text=True,
                    cwd=directory,
                    env={"PATH": os.environ.get("PATH", ""), "PYTHONNOUSERSITE": "1"},
                    timeout=self.timeout_seconds,
                    check=False,
                )
                return RunResult(completed.returncode, completed.stdout, completed.stderr, False, int((time.monotonic()-timer)*1000))
            except subprocess.TimeoutExpired as error:
                return RunResult(-1, error.stdout or "", error.stderr or "timeout", True, int((time.monotonic()-timer)*1000))
