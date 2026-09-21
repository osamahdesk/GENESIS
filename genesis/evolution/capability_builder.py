from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from genesis.core import PermissionPolicy


@dataclass(frozen=True, slots=True)
class CapabilityProposal:
    name: str
    purpose: str
    libraries: tuple[str, ...]
    status: str = "candidate"

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "purpose": self.purpose,
            "libraries": list(self.libraries),
            "status": self.status,
        }


class AIBuilder:
    """Creates reviewable project proposals; it never executes generated code."""

    def propose_model_project(self, policy: PermissionPolicy, output_dir: str | Path) -> CapabilityProposal:
        libraries = tuple(name for name, enabled in policy.capabilities.items() if enabled and name != "ai_builder")
        if not policy.capabilities.get("ai_builder", False):
            raise PermissionError("Enable the AI Builder capability from the dashboard first")
        if not libraries:
            raise ValueError("Enable at least one model library before creating a proposal")
        proposal = CapabilityProposal(
            name="generated-model-project",
            purpose="A reviewable local model project generated inside the GENESIS sandbox.",
            libraries=libraries,
        )
        target = Path(output_dir)
        target.mkdir(parents=True, exist_ok=True)
        (target / "proposal.json").write_text(json.dumps(proposal.as_dict(), indent=2) + "\n", encoding="utf-8")
        (target / "README.md").write_text(
            "# Generated Model Project\n\nThis is a candidate proposal. Review and evaluate it before execution.\n",
            encoding="utf-8",
        )
        return proposal
