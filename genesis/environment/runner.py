from __future__ import annotations

import os
import subprocess
import sys
import tempfile
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
    """A bounded local runner; not a perfect security sandbox."""

    def __init__(self, timeout_seconds: int = 10):
        self.timeout_seconds = timeout_seconds

    def run(self, source: str, stdin: str = "") -> RunResult:
        with tempfile.TemporaryDirectory(prefix="genesis-run-") as directory:
            path = Path(directory) / "solution.py"
            path.write_text(source, encoding="utf-8")
            env = {"PATH": os.environ.get("PATH", ""), "PYTHONNOUSERSITE": "1"}
            command = [sys.executable, "-I", str(path)]
            timer = __import__("time").monotonic()
            try:
                completed = subprocess.run(
                    command,
                    input=stdin,
                    capture_output=True,
                    text=True,
                    cwd=directory,
                    env=env,
                    timeout=self.timeout_seconds,
                    check=False,
                )
                return RunResult(
                    completed.returncode,
                    completed.stdout,
                    completed.stderr,
                    False,
                    int((__import__("time").monotonic() - timer) * 1000),
                )
            except subprocess.TimeoutExpired as error:
                return RunResult(
                    -1,
                    error.stdout or "",
                    error.stderr or "timeout",
                    True,
                    int((__import__("time").monotonic() - timer) * 1000),
                )
