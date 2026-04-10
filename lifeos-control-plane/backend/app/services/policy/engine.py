from app.config import settings
from app.core.enums import RiskLevel


RISK_BY_ACTION = {
    "github.fetch_issues": RiskLevel.LOW.value,
    "github.summarize_repo_context": RiskLevel.LOW.value,
    "task.create_checklist": RiskLevel.MEDIUM.value,
    "task.list_tasks": RiskLevel.LOW.value,
    "calendar.read_availability": RiskLevel.LOW.value,
    "calendar.suggest_slots": RiskLevel.MEDIUM.value,
    "email.draft": RiskLevel.MEDIUM.value,
    "email.send": RiskLevel.HIGH.value,
    "calendar.create_event": RiskLevel.HIGH.value,
}


def evaluate_action(action_type: str) -> dict[str, str | bool]:
    risk = RISK_BY_ACTION.get(action_type, RiskLevel.LOW.value)
    if risk == RiskLevel.HIGH.value:
        if action_type == "email.send" and not settings.enable_high_risk_actions:
            return {"risk_level": risk, "decision": "BLOCKED", "requires_approval": False}
        return {"risk_level": risk, "decision": "APPROVAL_REQUIRED", "requires_approval": True}
    return {"risk_level": risk, "decision": "ALLOWED", "requires_approval": False}
