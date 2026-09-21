from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SkillContract:
    input_schema: str
    output_schema: str
    preconditions: tuple[str, ...] = ()
    permissions: tuple[str, ...] = ()
    risk_level: str = "low"
    estimated_cost: float = 0.0
    timeout_seconds: int = 30
    evaluation: str = "caller-defined"
    rollback: str = "discard sandbox artifacts"

    def __post_init__(self) -> None:
        if self.risk_level not in {"low", "medium", "high"}:
            raise ValueError("risk_level must be low, medium, or high")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")


@dataclass(frozen=True, slots=True)
class ContractedSkill:
    definition_id: str
    contract: SkillContract

    def can_run(self, granted_permissions: set[str]) -> bool:
        return set(self.contract.permissions).issubset(granted_permissions)
