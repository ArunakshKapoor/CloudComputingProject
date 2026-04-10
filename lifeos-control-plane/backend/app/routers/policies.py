from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models.policy import PolicyRule
from app.dependencies import get_db
from app.schemas.policy import PolicyEvaluationRequest, PolicyRuleOut
from app.services.policy.engine import evaluate_action

router = APIRouter(prefix="/policies", tags=["policies"])


@router.get("", response_model=list[PolicyRuleOut])
def list_policies(db: Session = Depends(get_db)):
    rules = db.query(PolicyRule).all()
    return [PolicyRuleOut(action_type=r.action_type, risk_level=r.risk_level, requires_approval=r.requires_approval, allowed=r.allowed, reason_template=r.reason_template) for r in rules]


@router.post("/evaluate")
def evaluate(payload: PolicyEvaluationRequest):
    return evaluate_action(payload.action_type)
