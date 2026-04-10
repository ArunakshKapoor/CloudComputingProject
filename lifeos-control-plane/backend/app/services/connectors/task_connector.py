from app.services.connectors.base import BaseConnector


class TaskConnector(BaseConnector):
    name = "task"

    def health_check(self) -> dict:
        return {"name": self.name, "mode": "mock", "status": "ok"}

    def simulate(self, action_type: str, payload: dict) -> dict:
        return {"preview": ["Draft summary", "Assign owners", "Follow up"]}

    def execute(self, action_type: str, payload: dict) -> dict:
        return {"tasks": ["Summarize decisions", "Prepare follow-up", "Track blockers"]}
