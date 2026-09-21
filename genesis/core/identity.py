from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ExperimentIdentity:
    genesis_version: str
    model_version: str
    skills_version: str
    workflow_version: str
    policy_version: str
    tools: tuple[str, ...] = ()
    environment: str = "local"
    seed: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def fingerprint(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self) | {"fingerprint": self.fingerprint()}
