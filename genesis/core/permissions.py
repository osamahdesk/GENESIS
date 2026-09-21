from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(slots=True)
class PermissionPolicy:
    """Explicit, deny-by-default permissions for GENESIS tools."""

    network: str = "none"
    filesystem: str = "project_only"
    shell: bool = False
    private_data: bool = False
    external_actions: bool = False
    user_confirmed: bool = False

    def grant_project_filesystem(self) -> None:
        self.filesystem = "project_only"
        self.user_confirmed = True

    def grant_read_only_network(self) -> None:
        self.network = "read_only"
        self.user_confirmed = True

    def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(asdict(self), indent=2) + "\n", encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "PermissionPolicy":
        target = Path(path)
        if not target.exists():
            return cls()
        return cls(**json.loads(target.read_text(encoding="utf-8")))
