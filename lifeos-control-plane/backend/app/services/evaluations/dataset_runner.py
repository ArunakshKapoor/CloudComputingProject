import json
import re
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from app.services.evaluations.graders import grade
from app.services.evaluations.report_generator import summarize
from app.services.orchestration.executor import execute_step
from app.services.orchestration.planner import get_planner_provider
from app.services.policy.engine import evaluate_action
from app.services.simulation.simulator import simulate


@dataclass
class EvalStep:
    id: str
    name: str
    service: str
    action_type: str
    risk_level: str
    policy_decision: str
    approval_status: str = "NOT_REQUIRED"
    execution_status: str = "PLANNED"


def extract_repo_name(text: str) -> str:
    match = re.search(r"\b([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\b", text)
    return match.group(1) if match else "octocat/hello-world"


def build_eval_payload(prompt: str, step: EvalStep) -> dict:
    text = prompt.lower()

    recipient = "professor" if "professor" in text else "team" if "team" in text else "recipient"
    event_title = "Project Sync" if "project sync" in text else "Meeting"
    event_time_hint = "Tomorrow at 9 AM" if "tomorrow at" in text or "meeting" in text else "Afternoons next week"

    return {
        "workflow_id": f"eval-{step.id}",
        "user_id": "eval-user",
        "request_text": prompt,
        "step_id": step.id,
        "step_name": step.name,
        "action_type": step.action_type,
        "repo_name": extract_repo_name(prompt),
        "preferred_meeting_time": "Afternoons on weekdays",
        "email_recipient": recipient,
        "email_subject": "Follow-up from project sync",
        "email_body": f"Hi {recipient},\n\nFollowing up regarding: {prompt}\n\nBest regards,",
        "event_title": event_title,
        "event_time_hint": event_time_hint,
        "memory_context": {},
    }


def evaluate_prompt(prompt: str) -> dict:
    provider = get_planner_provider()
    raw_steps = provider.plan(prompt, memory_context={})

    steps: list[EvalStep] = []
    for idx, raw in enumerate(raw_steps):
        policy = evaluate_action(raw.action_type)
        steps.append(
            EvalStep(
                id=f"eval-step-{idx + 1}",
                name=raw.name,
                service=raw.service,
                action_type=raw.action_type,
                risk_level=str(policy["risk_level"]),
                policy_decision=str(policy["decision"]),
                approval_status="PENDING" if policy["requires_approval"] else "NOT_REQUIRED",
            )
        )

    simulation = simulate(steps)

    hard_failure = False
    success_count = 0

    for step in steps:
        if step.policy_decision == "BLOCKED":
            step.execution_status = "SKIPPED"
            continue

        if step.policy_decision == "APPROVAL_REQUIRED":
            # Auto-approve inside evaluation so we can exercise the execution path
            step.approval_status = "APPROVED"

        try:
            payload = build_eval_payload(prompt, step)
            result = execute_step(step, payload)
            step.execution_status = "FAILED" if result.get("status") == "blocked" else "SUCCEEDED"
        except Exception:
            hard_failure = True
            step.execution_status = "FAILED"

        if step.execution_status == "SUCCEEDED":
            success_count += 1

    workflow_status = "COMPLETED" if success_count == len(steps) else "PARTIALLY_COMPLETED"

    return {
        "prompt": prompt,
        "status": workflow_status,
        "estimated_latency_ms": simulation["estimated_latency_ms"],
        "estimated_cost_usd": simulation["estimated_cost_usd"],
        "hard_failure": hard_failure,
        "steps": [
            {
                "id": step.id,
                "name": step.name,
                "service": step.service,
                "action_type": step.action_type,
                "risk_level": step.risk_level,
                "policy_decision": step.policy_decision,
                "approval_status": step.approval_status,
                "execution_status": step.execution_status,
            }
            for step in steps
        ],
    }


def run_dataset(dataset: str) -> dict:
    path = Path(__file__).resolve().parents[4] / "evals" / "datasets" / f"{dataset}.json"
    prompts = json.loads(path.read_text())

    details = []
    metrics = []

    for item in prompts:
        result = evaluate_prompt(item["prompt"])
        details.append(result)
        metrics.append(grade(item["prompt"], result))

    return {
        "run_id": str(uuid4()),
        "status": "done",
        "dataset": dataset,
        "metrics": summarize(metrics),
        "details": details,
    }
