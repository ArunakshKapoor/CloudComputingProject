from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.enums import StepState, WorkflowStatus
from app.core.state_machine import can_transition
from app.core.utils import utc_now
from app.db.models.approval import Approval
from app.db.models.memory import Memory
from app.db.models.workflow import WorkflowRun, WorkflowStep
from app.dependencies import get_db
from app.schemas.simulation import SimulationResult
from app.schemas.workflow import WorkflowCreateRequest, WorkflowOut, WorkflowStepOut
from app.services.observability.tracer import trace
from app.services.orchestration.executor import execute_step
from app.services.orchestration.planner import get_planner_provider
from app.services.policy.engine import evaluate_action
from app.services.simulation.simulator import simulate

router = APIRouter(prefix="/workflows", tags=["workflows"])


def serialize_workflow(db: Session, wf: WorkflowRun) -> WorkflowOut:
    steps = db.query(WorkflowStep).filter(WorkflowStep.workflow_id == wf.id).all()
    return WorkflowOut(
        id=wf.id,
        user_id=wf.user_id,
        request_text=wf.request_text,
        mode=wf.mode,
        status=wf.status,
        estimated_latency_ms=wf.estimated_latency_ms,
        estimated_cost_usd=wf.estimated_cost_usd,
        created_at=wf.created_at,
        updated_at=wf.updated_at,
        steps=[WorkflowStepOut(**s.__dict__) for s in steps],
    )


@router.post("", response_model=WorkflowOut)
def create_workflow(payload: WorkflowCreateRequest, db: Session = Depends(get_db)):
    wf = WorkflowRun(id=str(uuid4()), user_id=payload.user_id, request_text=payload.request_text, mode=payload.mode, status=WorkflowStatus.CREATED.value)
    db.add(wf)
    db.commit()
    trace(db, wf.id, "workflow", "workflow_created", "Workflow created", {"mode": wf.mode})
    return serialize_workflow(db, wf)


@router.get("", response_model=list[WorkflowOut])
def list_workflows(db: Session = Depends(get_db)):
    return [serialize_workflow(db, w) for w in db.query(WorkflowRun).order_by(WorkflowRun.created_at.desc()).all()]


@router.get("/{workflow_id}", response_model=WorkflowOut)
def get_workflow(workflow_id: str, db: Session = Depends(get_db)):
    wf = db.get(WorkflowRun, workflow_id)
    if not wf:
        raise HTTPException(404, "workflow not found")
    return serialize_workflow(db, wf)


@router.post("/{workflow_id}/plan", response_model=WorkflowOut)
def plan_workflow(workflow_id: str, db: Session = Depends(get_db)):
    wf = db.get(WorkflowRun, workflow_id)
    if not wf:
        raise HTTPException(404, "workflow not found")
    if not can_transition(WorkflowStatus(wf.status), WorkflowStatus.PLANNING):
        raise HTTPException(400, "invalid transition")
    wf.status = WorkflowStatus.PLANNING.value
    provider = get_planner_provider()
    memories = db.query(Memory).filter(Memory.user_id == wf.user_id).all()
    trace(db, wf.id, "memory", "memory_retrieved", f"Retrieved {len(memories)} memories")
    for raw in provider.plan(wf.request_text):
        policy = evaluate_action(raw.action_type)
        step = WorkflowStep(
            id=str(uuid4()), workflow_id=wf.id, name=raw.name, service=raw.service, action_type=raw.action_type,
            depends_on_json="[]", risk_level=str(policy["risk_level"]), policy_decision=str(policy["decision"]),
            approval_status="PENDING" if policy["requires_approval"] else "NOT_REQUIRED",
            execution_status=StepState.PLANNED.value,
        )
        db.add(step)
        if policy["requires_approval"]:
            db.add(Approval(workflow_id=wf.id, step_id=step.id, status="PENDING"))
    wf.status = WorkflowStatus.POLICY_REVIEW.value
    wf.updated_at = utc_now()
    db.commit()
    trace(db, wf.id, "planning", "plan_created", "Plan and policy decisions generated")
    return serialize_workflow(db, wf)


@router.post("/{workflow_id}/simulate", response_model=SimulationResult)
def simulate_workflow(workflow_id: str, db: Session = Depends(get_db)):
    wf = db.get(WorkflowRun, workflow_id)
    if not wf:
        raise HTTPException(404, "workflow not found")
    steps = db.query(WorkflowStep).filter(WorkflowStep.workflow_id == wf.id).all()
    output = simulate(steps)
    wf.status = WorkflowStatus.SIMULATING.value
    wf.estimated_latency_ms = output["estimated_latency_ms"]
    wf.estimated_cost_usd = output["estimated_cost_usd"]
    if any(s.policy_decision == "APPROVAL_REQUIRED" for s in steps):
        wf.status = WorkflowStatus.WAITING_FOR_APPROVAL.value
    else:
        wf.status = WorkflowStatus.APPROVED_FOR_EXECUTION.value
    db.commit()
    trace(db, wf.id, "simulation", "simulation_completed", "Simulation completed", output)
    return SimulationResult(**output)


@router.post("/{workflow_id}/execute", response_model=WorkflowOut)
def execute_workflow(workflow_id: str, db: Session = Depends(get_db)):
    wf = db.get(WorkflowRun, workflow_id)
    if not wf:
        raise HTTPException(404, "workflow not found")
    steps = db.query(WorkflowStep).filter(WorkflowStep.workflow_id == wf.id).all()
    pending_approvals = db.query(Approval).filter(Approval.workflow_id == wf.id, Approval.status == "PENDING").count()
    if pending_approvals > 0:
        raise HTTPException(400, "approvals pending")
    wf.status = WorkflowStatus.EXECUTING.value
    success = 0
    for step in steps:
        if step.policy_decision == "BLOCKED":
            step.execution_status = StepState.SKIPPED.value
            continue
        if step.approval_status == "REJECTED":
            step.execution_status = StepState.SKIPPED.value
            continue
        trace(db, wf.id, "execution", "step_execution_started", f"Executing {step.action_type}", step_id=step.id)
        result = execute_step(step, {})
        step.execution_status = StepState.SUCCEEDED.value if result.get("status") != "blocked" else StepState.FAILED.value
        step.output_summary = str(result)
        success += 1 if step.execution_status == StepState.SUCCEEDED.value else 0
        trace(db, wf.id, "execution", "step_succeeded", f"Finished {step.action_type}", {"result": result}, step.id)
    wf.status = WorkflowStatus.COMPLETED.value if success == len(steps) else WorkflowStatus.PARTIALLY_COMPLETED.value
    wf.completed_at = utc_now()
    db.commit()
    trace(db, wf.id, "workflow", "workflow_completed", f"Workflow ended with {wf.status}")
    return serialize_workflow(db, wf)


@router.post("/{workflow_id}/cancel", response_model=WorkflowOut)
def cancel_workflow(workflow_id: str, db: Session = Depends(get_db)):
    wf = db.get(WorkflowRun, workflow_id)
    if not wf:
        raise HTTPException(404, "workflow not found")
    wf.status = WorkflowStatus.CANCELLED.value
    wf.updated_at = utc_now()
    db.commit()
    trace(db, wf.id, "workflow", "workflow_cancelled", "Workflow cancelled")
    return serialize_workflow(db, wf)
