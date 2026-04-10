from datetime import datetime
from pydantic import BaseModel, Field


class WorkflowCreateRequest(BaseModel):
    user_id: str = "demo-user"
    request_text: str
    mode: str = "mock"


class WorkflowStepOut(BaseModel):
    id: str
    name: str
    service: str
    action_type: str
    risk_level: str
    policy_decision: str
    approval_status: str
    execution_status: str
    output_summary: str


class WorkflowOut(BaseModel):
    id: str
    user_id: str
    request_text: str
    mode: str
    status: str
    estimated_latency_ms: int
    estimated_cost_usd: float
    created_at: datetime
    updated_at: datetime
    steps: list[WorkflowStepOut] = Field(default_factory=list)
