from __future__ import annotations

from dataclasses import dataclass

from genesis.memory import StrategyMemory
from genesis.skills import SkillDefinition, SkillRegistry


@dataclass(frozen=True, slots=True)
class DynamicPlan:
    task_signature: str
    objective: str
    skill_ids: tuple[str, ...]
    steps: tuple[str, ...]
    recalled_lessons: tuple[str, ...]
    risk_levels: tuple[str, ...]


class DynamicPlanner:
    def __init__(self, skills: SkillRegistry | None = None, memory: StrategyMemory | None = None) -> None:
        self.skills = skills or SkillRegistry()
        self.memory = memory or StrategyMemory()

    def plan(self, task_signature: str, objective: str) -> DynamicPlan:
        selected: tuple[SkillDefinition, ...] = self.skills.select_for(objective)
        lessons = self.memory.lessons_for(task_signature)
        steps = ["define_success_criteria"]
        steps.extend(f"use:{skill.id}" for skill in selected)
        if lessons:
            steps.append("apply_recalled_lessons")
        steps.extend(("execute_candidate", "evaluate_independently", "record_lesson"))
        return DynamicPlan(
            task_signature,
            objective,
            tuple(skill.id for skill in selected),
            tuple(steps),
            lessons,
            tuple(skill.risk_level for skill in selected),
        )
