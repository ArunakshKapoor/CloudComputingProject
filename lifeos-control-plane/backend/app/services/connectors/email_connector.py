from app.config import settings
from app.services.connectors.base import BaseConnector


class EmailConnector(BaseConnector):
    name = "email"

    def health_check(self) -> dict:
        return {"name": self.name, "mode": "mock", "status": "ok"}

    def simulate(self, action_type: str, payload: dict) -> dict:
        return {"subject": "Follow-up from project sync", "body": "Hi team, thanks for today's sync..."}

    def execute(self, action_type: str, payload: dict) -> dict:
        if action_type == "email.send" and not settings.enable_high_risk_actions:
            return {"status": "blocked", "reason": "HIGH risk disabled"}
        return {"status": "ok", "message": "Draft generated"}
