from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

DEVELOPMENT_CAPABILITIES = (
    "transformers",
    "pytorch",
    "huggingface",
    "ai_builder",
    "model_training",
)


@dataclass(slots=True)
class PermissionPolicy:
    """Explicit, deny-by-default permissions and development capabilities."""

    network: str = "none"
    filesystem: str = "project_only"
    shell: bool = False
    private_data: bool = False
    external_actions: bool = False
    user_confirmed: bool = False
    capabilities: dict[str, bool] = field(default_factory=lambda: {name: False for name in DEVELOPMENT_CAPABILITIES})

    def __post_init__(self) -> None:
        for name in DEVELOPMENT_CAPABILITIES:
            self.capabilities.setdefault(name, False)

    def grant_project_filesystem(self) -> None:
        self.filesystem = "project_only"
        self.user_confirmed = True

    def grant_read_only_network(self) -> None:
        self.network = "read_only"
        self.user_confirmed = True

    def toggle_capability(self, name: str, enabled: bool) -> None:
        if name not in DEVELOPMENT_CAPABILITIES:
            raise ValueError(f"Unknown development capability: {name}")
        self.capabilities[name] = bool(enabled)
        self.user_confirmed = True

    def as_dict(self) -> dict[str, object]:
        return asdict(self)

    def save(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self.as_dict(), indent=2) + "\n", encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> PermissionPolicy:
        target = Path(path)
        if not target.exists():
            return cls()
        return cls(**json.loads(target.read_text(encoding="utf-8")))
