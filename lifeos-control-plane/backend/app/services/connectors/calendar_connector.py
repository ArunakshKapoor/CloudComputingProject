from app.services.connectors.base import BaseConnector


class CalendarConnector(BaseConnector):
    name = "calendar"

    def health_check(self) -> dict:
        return {"name": self.name, "mode": "mock", "status": "ok"}

    def simulate(self, action_type: str, payload: dict) -> dict:
        pref = payload.get("preferred_meeting_time", "Afternoons on weekdays")
        return {"preview": f"Based on preference '{pref}': Tue 2 PM, Thu 3:30 PM"}

    def execute(self, action_type: str, payload: dict) -> dict:
        return {"slots": ["Tue 2:00 PM", "Thu 3:30 PM"]}
