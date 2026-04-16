from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class PlannedStep:
    name: str
    service: str
    action_type: str
    depends_on: list[int]


def has_any(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def get_memory(memory_context: dict | None, key: str, default=None):
    if not memory_context:
        return default
    value = memory_context.get(key, default)
    return value if value not in (None, "") else default


def extract_repo_name(text: str, memory_context: dict | None = None) -> str | None:
    remembered_repo = get_memory(memory_context, "github_repo")
    if remembered_repo:
        return remembered_repo

    match = re.search(r"\b([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\b", text)
    return match.group(1) if match else None


def extract_recipient(text: str, memory_context: dict | None = None) -> str:
    remembered_recipient = get_memory(memory_context, "default_email_recipient")
    if remembered_recipient:
        return remembered_recipient

    match = re.search(r"\bto ([a-zA-Z][a-zA-Z\s]+)", text)
    if match:
        candidate = match.group(1).strip()
        candidate = re.split(r"\b(confirming|about|regarding|for|tomorrow|next)\b", candidate)[0].strip()
        if candidate:
            return candidate

    if "professor" in text:
        return "professor"
    if "team" in text:
        return "team"

    return "recipient"


def extract_event_time_hint(text: str, memory_context: dict | None = None) -> str:
    remembered_time = get_memory(memory_context, "preferred_event_time")
    if remembered_time:
        return remembered_time

    patterns = [
        r"(tomorrow at [^,.]+)",
        r"(today at [^,.]+)",
        r"(next monday at [^,.]+)",
        r"(next tuesday at [^,.]+)",
        r"(next wednesday at [^,.]+)",
        r"(next thursday at [^,.]+)",
        r"(next friday at [^,.]+)",
        r"(next week[^,.]*)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()

    return "Tomorrow at 9 AM"


def extract_event_title(text: str, memory_context: dict | None = None) -> str:
    remembered_title = get_memory(memory_context, "default_event_title")
    if remembered_title:
        return remembered_title

    if "project sync" in text:
        return "Project Sync"
    if "meeting" in text:
        return "Meeting"
    if "interview" in text:
        return "Interview"

    return "Scheduled Event"


def mentions_fixed_time(text: str) -> bool:
    return has_any(
        text,
        [
            "tomorrow at",
            "today at",
            "next monday at",
            "next tuesday at",
            "next wednesday at",
            "next thursday at",
            "next friday at",
            " at 9",
            " at 10",
            " at 11",
            " at 12",
            " at 1",
            " at 2",
            " at 3",
            " at 4",
            " at 5",
            " at 6",
            " at 7",
            " at 8",
            " am",
            " pm",
        ],
    )


class MockPlannerProvider:
    """Deterministic planner with richer intent extraction and memory-aware naming."""

    def plan(self, request_text: str, memory_context: dict | None = None) -> list[PlannedStep]:
        text = " ".join(request_text.lower().split())
        steps: list[PlannedStep] = []

        repo_name = extract_repo_name(text, memory_context)
        recipient = extract_recipient(text, memory_context)
        preferred_meeting_time = get_memory(memory_context, "preferred_meeting_time", "Afternoons on weekdays")
        event_title = extract_event_title(text, memory_context)
        event_time_hint = extract_event_time_hint(text, memory_context)

        # --------
        # Intents
        # --------
        asks_email = has_any(text, ["email", "mail", "follow-up", "follow up"])
        asks_send = asks_email and has_any(text, ["send", "email to", "mail to"])
        asks_draft = asks_email and has_any(text, ["draft", "write", "compose", "follow-up", "follow up"])

        asks_calendar = has_any(text, ["calendar", "meeting", "slot", "slots", "event", "schedule", "availability"])
        asks_create_event = asks_calendar and (
            has_any(
                text,
                [
                    "create a calendar event",
                    "create calendar event",
                    "calendar event",
                    "create event",
                    "schedule a meeting",
                    "schedule meeting",
                    "book a meeting",
                    "book meeting",
                ],
            )
            or mentions_fixed_time(text)
        )

        asks_suggest_slots = asks_calendar and has_any(
            text,
            [
                "suggest",
                "slots",
                "availability",
                "meeting slots",
                "available time",
                "two meeting slots",
            ],
        )

        asks_tasks = has_any(
            text,
            [
                "task",
                "tasks",
                "checklist",
                "todo",
                "to-do",
                "action items",
                "next steps",
            ],
        )

        asks_github = has_any(text, ["github", "repo", "repository", "issue", "issues"]) or (
            repo_name is not None and has_any(text, ["project", "codebase", "bug", "release"])
        )

        asks_issue_summary = asks_github and has_any(
            text,
            [
                "summarize",
                "summary",
                "top open issues",
                "open issues",
                "issues",
                "bugs",
            ],
        )

        # --------
        # Build steps
        # --------

        if asks_send:
            draft_idx = len(steps)
            steps.append(
                PlannedStep(
                    name=f"Draft confirmation email to {recipient}",
                    service="email",
                    action_type="email.draft",
                    depends_on=[],
                )
            )
            steps.append(
                PlannedStep(
                    name=f"Send confirmation email to {recipient}",
                    service="email",
                    action_type="email.send",
                    depends_on=[draft_idx],
                )
            )
        elif asks_draft or asks_email:
            steps.append(
                PlannedStep(
                    name=f"Draft follow-up email to {recipient}",
                    service="email",
                    action_type="email.draft",
                    depends_on=[],
                )
            )

        if asks_create_event:
            steps.append(
                PlannedStep(
                    name=f"Create calendar event: {event_title} ({event_time_hint})",
                    service="calendar",
                    action_type="calendar.create_event",
                    depends_on=[],
                )
            )
        elif asks_suggest_slots or asks_calendar:
            steps.append(
                PlannedStep(
                    name=f"Suggest meeting slots ({preferred_meeting_time})",
                    service="calendar",
                    action_type="calendar.suggest_slots",
                    depends_on=[],
                )
            )

        if asks_tasks:
            task_name = "Create action checklist" if has_any(text, ["action items", "next steps"]) else "Create checklist"
            steps.append(
                PlannedStep(
                    name=task_name,
                    service="task",
                    action_type="task.create_checklist",
                    depends_on=[],
                )
            )

        if asks_issue_summary or asks_github:
            repo_label = repo_name or "configured repository"
            steps.append(
                PlannedStep(
                    name=f"Summarize open issues in {repo_label}",
                    service="github",
                    action_type="github.fetch_issues",
                    depends_on=[],
                )
            )

        return steps or [PlannedStep("List tasks", "task", "task.list_tasks", [])]