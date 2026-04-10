from pydantic import BaseModel


class PolicyRuleOut(BaseModel):
    action_type: str
    risk_level: str
    requires_approval: bool
    allowed: bool
    reason_template: str


class PolicyEvaluationRequest(BaseModel):
    action_type: str
