from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlannedStep:
    name: str
    service: str
    action_type: str
    depends_on: list[int]

def has_any(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)


class MockPlannerProvider:
    """Deterministic planner for demo prompts with basic intent detection."""

    def plan(self, request_text: str) -> list[PlannedStep]:
        text = " ".join(request_text.lower().split())
        steps: list[PlannedStep] = []

        # --------
        # Email intent
        # --------
        wants_email = has_any(text, ["email", "mail"])
        wants_send_email = wants_email and has_any(
            text,
            [
                "send an email",
                "send email",
                "send the email",
                "email to",
                "mail to",
                "send ",
            ],
        )
        wants_draft_email = wants_email and has_any(
            text,
            [
                "draft",
                "write an email",
                "compose",
                "follow-up email",
                "follow up email",
            ],
        )

        # --------
        # Calendar intent
        # --------
        wants_calendar = has_any(text, ["calendar", "meeting", "slot", "event", "schedule"])

        wants_create_event = has_any(
            text,
            [
                "create a calendar event",
                "create calendar event",
                "calendar event",
                "create an event",
                "create event",
                "schedule a meeting",
                "schedule meeting",
                "book a meeting",
                "book meeting",
            ],
        ) or (
            wants_calendar
            and (
                "tomorrow at" in text
                or "today at" in text
                or "next monday at" in text
                or "next tuesday at" in text
                or "next wednesday at" in text
                or "next thursday at" in text
                or "next friday at" in text
                or " at 9" in text
                or " at 10" in text
                or " at 11" in text
                or " at 12" in text
                or " at 1" in text
                or " at 2" in text
                or " at 3" in text
                or " at 4" in text
                or " at 5" in text
                or " at 6" in text
                or " at 7" in text
                or " at 8" in text
            )
        )

        wants_suggest_slots = wants_calendar and has_any(
            text,
            [
                "suggest",
                "slot",
                "slots",
                "availability",
                "available time",
                "meeting time",
            ],
        )

        # --------
        # Task intent
        # --------
        wants_tasks = has_any(text, ["task", "tasks", "checklist", "todo", "to-do"])

        # --------
        # GitHub intent
        # --------
        wants_github = has_any(text, ["github", "repo", "repository", "issue", "issues"])

        # --------
        # Build steps
        # --------

        # Email logic:
        # - If the user explicitly wants to send an email, create BOTH a draft step and a send step.
        #   This preserves previewability while also triggering governance on the send action.
        # - If the user only wants a draft, create only the draft step.
        if wants_send_email:
            draft_idx = len(steps)
            steps.append(
                PlannedStep(
                    name="Draft confirmation email",
                    service="email",
                    action_type="email.draft",
                    depends_on=[],
                )
            )
            steps.append(
                PlannedStep(
                    name="Send confirmation email",
                    service="email",
                    action_type="email.send",
                    depends_on=[draft_idx],
                )
            )
        elif wants_draft_email or wants_email:
            steps.append(
                PlannedStep(
                    name="Draft follow-up email",
                    service="email",
                    action_type="email.draft",
                    depends_on=[],
                )
            )

        # Calendar logic:
        # - Explicit event creation or fixed-time scheduling should map to HIGH-risk create_event
        # - Otherwise, slot-finding remains a medium-risk suggestion flow
        if wants_create_event:
            steps.append(
                PlannedStep(
                    name="Create calendar event",
                    service="calendar",
                    action_type="calendar.create_event",
                    depends_on=[],
                )
            )
        elif wants_suggest_slots or wants_calendar:
            steps.append(
                PlannedStep(
                    name="Suggest meeting slots",
                    service="calendar",
                    action_type="calendar.suggest_slots",
                    depends_on=[],
                )
            )

        if wants_tasks:
            steps.append(
                PlannedStep(
                    name="Create checklist",
                    service="task",
                    action_type="task.create_checklist",
                    depends_on=[],
                )
            )

        if wants_github:
            steps.append(
                PlannedStep(
                    name="Summarize open issues",
                    service="github",
                    action_type="github.fetch_issues",
                    depends_on=[],
                )
            )

        return steps or [PlannedStep("List tasks", "task", "task.list_tasks", [])]
