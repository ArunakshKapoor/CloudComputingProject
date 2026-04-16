from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.utils import utc_now
from app.db.models.approval import Approval
from app.db.models.workflow import WorkflowStep
from app.dependencies import get_db
from app.schemas.approval import ApprovalDecisionRequest, ApprovalOut
from app.services.observability.tracer import trace

router = APIRouter(tags=["approvals"])


@router.get("/workflows/{workflow_id}/approvals", response_model=list[ApprovalOut])
def list_approvals(workflow_id: str, db: Session = Depends(get_db)):
    rows = db.query(Approval).filter(Approval.workflow_id == workflow_id).all()
    output = []

    for a in rows:
        step = db.get(WorkflowStep, a.step_id)
        output.append(
            ApprovalOut(
                id=a.id,
                workflow_id=a.workflow_id,
                step_id=a.step_id,
                status=a.status,
                decision_comment=a.decision_comment,
                step_name=step.name if step else None,
                action_type=step.action_type if step else None,
                risk_level=step.risk_level if step else None,
            )
        )

    return output


@router.post("/approvals/{step_id}", response_model=ApprovalOut)
def decide(step_id: str, payload: ApprovalDecisionRequest, db: Session = Depends(get_db)):
    approval = db.query(Approval).filter(Approval.step_id == step_id).first()
    if not approval:
        raise HTTPException(404, "approval not found")

    approval.status = payload.status
    approval.decision_comment = payload.decision_comment
    approval.decided_at = utc_now()

    step = db.get(WorkflowStep, step_id)
    if step:
        step.approval_status = payload.status
        trace(
            db,
            approval.workflow_id,
            "approval",
            "approval_decided",
            f"Step {step_id} {payload.status}",
            step_id=step_id,
        )

    db.commit()

    return ApprovalOut(
        id=approval.id,
        workflow_id=approval.workflow_id,
        step_id=approval.step_id,
        status=approval.status,
        decision_comment=approval.decision_comment,
        step_name=step.name if step else None,
        action_type=step.action_type if step else None,
        risk_level=step.risk_level if step else None,
    )