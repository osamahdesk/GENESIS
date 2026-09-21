from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time


root = tempfile.mkdtemp(prefix="genesis-cli-cache-")
results = []
for run_number in (1, 2):
    started = time.perf_counter()
    completed = subprocess.run(["python3", "-m", "genesis", "run", "--root", root], capture_output=True, text=True, check=True)
    elapsed = time.perf_counter() - started
    payload = json.loads(completed.stdout)
    results.append({"run": run_number, "wall_seconds": round(elapsed, 6), "cache_hit": payload["evaluation"].get("cache_hit", False), "score": payload["evaluation"]["score"]})
print(json.dumps(results, indent=2))
shutil.rmtree(root, ignore_errors=True)
