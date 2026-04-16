from app.services.connectors.base import BaseConnector


class TaskConnector(BaseConnector):
    name = "task"

    def health_check(self) -> dict:
        return {"name": self.name, "mode": "mock", "status": "ok"}

    def _tasks_from_payload(self, payload: dict) -> list[str]:
        request_text = str(payload.get("request_text", "")).lower()

        if "sync" in request_text or "meeting" in request_text:
            return [
                "Summarize decisions",
                "Confirm owners",
                "Send follow-up",
            ]

        if "github" in request_text or "issue" in request_text:
            return [
                "Review open issues",
                "Prioritize blockers",
                "Assign next actions",
            ]

        return [
            "Review request",
            "Break down actions",
            "Track completion",
        ]

    def simulate(self, action_type: str, payload: dict) -> dict:
        return {
            "action": action_type,
            "mode": "mock",
            "preview": self._tasks_from_payload(payload),
        }

    def execute(self, action_type: str, payload: dict) -> dict:
        return {
            "status": "ok",
            "mode": "mock",
            "tasks": self._tasks_from_payload(payload),
        }