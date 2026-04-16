from pydantic import BaseModel


class ApprovalDecisionRequest(BaseModel):
    status: str
    decision_comment: str = ""


class ApprovalOut(BaseModel):
    id: int
    workflow_id: str
    step_id: str
    status: str
    decision_comment: str
    step_name: str | None = None
    action_type: str | None = None
    risk_level: str | None = None
