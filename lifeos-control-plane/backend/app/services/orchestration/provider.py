from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlannedStep:
    name: str
    service: str
    action_type: str
    depends_on: list[int]


class MockPlannerProvider:
    """Deterministic planner for demo prompts."""

    def plan(self, request_text: str) -> list[PlannedStep]:
        text = request_text.lower()
        steps: list[PlannedStep] = []
        if "email" in text:
            steps.append(PlannedStep("Draft follow-up email", "email", "email.draft", []))
        if "meeting" in text or "slot" in text or "calendar" in text:
            steps.append(PlannedStep("Suggest meeting slots", "calendar", "calendar.suggest_slots", []))
        if "task" in text or "checklist" in text:
            steps.append(PlannedStep("Create checklist", "task", "task.create_checklist", []))
        if "github" in text or "repo" in text or "issue" in text:
            steps.append(PlannedStep("Summarize open issues", "github", "github.fetch_issues", []))
        return steps or [PlannedStep("List tasks", "task", "task.list_tasks", [])]
