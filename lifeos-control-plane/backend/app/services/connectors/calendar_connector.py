from app.services.connectors.base import BaseConnector


class CalendarConnector(BaseConnector):
    name = "calendar"

    def health_check(self) -> dict:
        return {"name": self.name, "mode": "mock", "status": "ok"}

    def _calendar_context(self, payload: dict) -> dict:
        return {
            "preferred_meeting_time": payload.get("preferred_meeting_time", "Afternoons on weekdays"),
            "event_title": payload.get("event_title", "Meeting"),
            "event_time_hint": payload.get("event_time_hint", "Tomorrow at 9 AM"),
        }

    def simulate(self, action_type: str, payload: dict) -> dict:
        context = self._calendar_context(payload)

        if action_type == "calendar.create_event":
            return {
                "action": action_type,
                "mode": "mock",
                "preview": f"Would create event '{context['event_title']}' at {context['event_time_hint']}.",
                **context,
            }

        return {
            "action": action_type,
            "mode": "mock",
            "preview": f"Based on preference '{context['preferred_meeting_time']}': Tue 2 PM, Thu 3:30 PM",
            **context,
        }

    def execute(self, action_type: str, payload: dict) -> dict:
        context = self._calendar_context(payload)

        if action_type == "calendar.create_event":
            return {
                "status": "ok",
                "mode": "mock",
                "event": {
                    "title": context["event_title"],
                    "time_hint": context["event_time_hint"],
                },
            }

        return {
            "status": "ok",
            "mode": "mock",
            "slots": ["Tue 2:00 PM", "Thu 3:30 PM"],
            "preferred_meeting_time": context["preferred_meeting_time"],
        }