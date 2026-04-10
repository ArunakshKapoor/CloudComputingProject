from app.db.models.workflow import WorkflowStep

COSTS = {"LOW": 0.001, "MEDIUM": 0.005, "HIGH": 0.01}
LAT = {"LOW": 200, "MEDIUM": 450, "HIGH": 700}


def preview_for_step(step: WorkflowStep) -> str:
    if step.action_type == "email.draft":
        return "Subject: Follow-up from project sync\\nBody: Thank you for today..."
    if step.action_type == "calendar.suggest_slots":
        return "Suggested slots: Tue 2:00 PM, Thu 3:30 PM"
    if step.action_type == "task.create_checklist":
        return "Checklist: [ ] Summarize actions [ ] Update docs [ ] Confirm owners"
    if step.action_type.startswith("github"):
        return "Top issues: #42 flaky tests, #77 auth timeout, #81 dashboard perf"
    return "Preview unavailable"


def simulate(steps: list[WorkflowStep]) -> dict:
    previews = []
    total_cost = 0.0
    total_latency = 0
    gated = 0
    for step in steps:
        total_cost += COSTS.get(step.risk_level, 0.001)
        total_latency += LAT.get(step.risk_level, 100)
        if step.policy_decision == "APPROVAL_REQUIRED":
            gated += 1
        previews.append({"step_id": step.id, "preview": preview_for_step(step), "approval_required": step.policy_decision == "APPROVAL_REQUIRED"})
    return {
        "estimated_latency_ms": total_latency,
        "estimated_cost_usd": round(total_cost, 4),
        "side_effect_summary": f"{gated} steps require approval before execution.",
        "steps": previews,
    }
