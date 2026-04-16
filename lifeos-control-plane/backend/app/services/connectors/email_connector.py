from app.config import settings
from app.services.connectors.base import BaseConnector


class EmailConnector(BaseConnector):
    name = "email"

    def health_check(self) -> dict:
        return {"name": self.name, "mode": "mock", "status": "ok"}

    def _draft_from_payload(self, payload: dict) -> dict:
        recipient = payload.get("email_recipient", "professor")
        subject = payload.get("email_subject", "Follow-up from project sync")
        body = payload.get("email_body", "Hi, thanks for today's discussion...")
        return {
            "recipient": recipient,
            "subject": subject,
            "body": body,
        }

    def simulate(self, action_type: str, payload: dict) -> dict:
        draft = self._draft_from_payload(payload)
        return {
            "action": action_type,
            "mode": "mock",
            **draft,
        }

    def execute(self, action_type: str, payload: dict) -> dict:
        draft = self._draft_from_payload(payload)

        if action_type == "email.send" and not settings.enable_high_risk_actions:
            return {
                "status": "blocked",
                "reason": "HIGH risk disabled",
                **draft,
            }

        if action_type == "email.draft":
            return {
                "status": "ok",
                "mode": "mock",
                "message": "Draft generated",
                **draft,
            }

        return {
            "status": "ok",
            "mode": "mock",
            "message": "Email action completed",
            **draft,
        }
