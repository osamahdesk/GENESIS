from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True, slots=True)
class EvidenceSource:
    id: str
    uri: str
    reliability: float
    published: date | None = None
    supports: bool = True

    def __post_init__(self) -> None:
        if not 0.0 <= self.reliability <= 1.0:
            raise ValueError("EvidenceSource.reliability must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class ClaimAssessment:
    claim: str
    confidence: float
    supporting_sources: tuple[str, ...]
    contradicting_sources: tuple[str, ...]
    status: str


@dataclass(slots=True)
class EvidenceGraph:
    claims: dict[str, list[EvidenceSource]] = field(default_factory=dict)

    def add(self, claim: str, source: EvidenceSource) -> None:
        if not claim.strip():
            raise ValueError("claim must not be empty")
        self.claims.setdefault(claim, []).append(source)

    def assess(self, claim: str) -> ClaimAssessment:
        sources = self.claims.get(claim, [])
        supporting = tuple(source.id for source in sources if source.supports)
        contradicting = tuple(source.id for source in sources if not source.supports)
        support_score = sum(source.reliability for source in sources if source.supports)
        contradict_score = sum(source.reliability for source in sources if not source.supports)
        total = support_score + contradict_score
        confidence = 0.0 if total == 0 else max(0.0, min(1.0, (support_score - contradict_score + total) / (2 * total)))
        status = "supported" if confidence >= 0.7 and not contradicting else "contested" if contradicting else "insufficient"
        return ClaimAssessment(claim, confidence, supporting, contradicting, status)
