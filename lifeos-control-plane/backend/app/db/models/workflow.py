from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.utils import utc_now


class Base(DeclarativeBase):
    pass


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    request_text: Mapped[str] = mapped_column(Text)
    mode: Mapped[str] = mapped_column(String, default="mock")
    status: Mapped[str] = mapped_column(String)
    estimated_latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    estimated_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    actual_latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    actual_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=utc_now)
    completed_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    workflow_id: Mapped[str] = mapped_column(String, ForeignKey("workflow_runs.id"))
    name: Mapped[str] = mapped_column(String)
    service: Mapped[str] = mapped_column(String)
    action_type: Mapped[str] = mapped_column(String)
    depends_on_json: Mapped[str] = mapped_column(String, default="[]")
    risk_level: Mapped[str] = mapped_column(String, default="LOW")
    policy_decision: Mapped[str] = mapped_column(String, default="ALLOWED")
    approval_status: Mapped[str] = mapped_column(String, default="NOT_REQUIRED")
    execution_status: Mapped[str] = mapped_column(String, default="PENDING")
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    output_summary: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=utc_now)
