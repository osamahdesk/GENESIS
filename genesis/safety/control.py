from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RiskDecision:
    action: str
    risk_level: str
    allowed: bool
    requires_approval: bool
    reason: str


@dataclass(slots=True)
class KillSwitch:
    path: Path
    _stopped: bool = field(default=False, init=False)

    def stop(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("STOP\n", encoding="utf-8")
        self._stopped = True

    def is_stopped(self) -> bool:
        return self._stopped or self.path.exists()

    def require_running(self) -> None:
        if self.is_stopped():
            raise RuntimeError("GENESIS execution stopped by external kill switch")


class PolicyEngine:
    def decide(self, action: str, risk_level: str, granted: set[str], required: set[str]) -> RiskDecision:
        if risk_level not in {"low", "medium", "high"}:
            raise ValueError("risk_level must be low, medium, or high")
        missing = required - granted
        if missing:
            return RiskDecision(action, risk_level, False, False, f"Missing permissions: {sorted(missing)}")
        if risk_level == "high":
            return RiskDecision(action, risk_level, False, True, "High-risk action requires human approval")
        return RiskDecision(action, risk_level, True, risk_level == "medium", "Allowed by policy")
