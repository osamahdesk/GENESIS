from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SkillDefinition:
    id: str
    name: str
    description: str
    triggers: tuple[str, ...]
    risk_level: str = "low"


class SkillRegistry:
    def __init__(self, skills: tuple[SkillDefinition, ...] = ()) -> None:
        self._skills: dict[str, SkillDefinition] = {skill.id: skill for skill in skills}

    def register(self, skill: SkillDefinition) -> None:
        if not skill.id.strip():
            raise ValueError("skill.id must not be empty")
        if skill.id in self._skills:
            raise ValueError(f"Skill already registered: {skill.id}")
        self._skills[skill.id] = skill

    def get(self, skill_id: str) -> SkillDefinition:
        try:
            return self._skills[skill_id]
        except KeyError as error:
            raise KeyError(f"Unknown skill: {skill_id}") from error

    def list(self) -> tuple[SkillDefinition, ...]:
        return tuple(self._skills.values())

    def select_for(self, task_text: str) -> tuple[SkillDefinition, ...]:
        text = task_text.casefold()
        selected = [
            skill for skill in self._skills.values()
            if any(trigger.casefold() in text for trigger in skill.triggers)
        ]
        if not selected:
            selected = [self._skills["reasoning"]]
        return tuple(selected)


def default_registry() -> SkillRegistry:
    return SkillRegistry(
        (
            SkillDefinition("reasoning", "Structured reasoning", "Break a task into testable steps.", ("problem", "plan", "reason")),
            SkillDefinition("coding", "Python coding", "Build and inspect executable Python artifacts.", ("python", "code", "program", "script")),
            SkillDefinition("research", "Web research", "Collect information and preserve provenance.", ("research", "source", "paper", "web")),
            SkillDefinition("data-analysis", "Data analysis", "Inspect structured data and produce measurements.", ("data", "csv", "table", "statistics")),
            SkillDefinition("verification", "Source verification", "Compare claims against independent evidence.", ("verify", "evidence", "contradiction", "claim")),
            SkillDefinition("tool-use", "Tool use", "Select bounded tools through explicit capability contracts.", ("tool", "api", "browser", "github"), "medium"),
        )
    )
