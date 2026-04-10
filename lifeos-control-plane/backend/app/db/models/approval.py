from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.workflow import Base


class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_id: Mapped[str] = mapped_column(String, ForeignKey("workflow_runs.id"))
    step_id: Mapped[str] = mapped_column(String, ForeignKey("workflow_steps.id"))
    status: Mapped[str] = mapped_column(String, default="PENDING")
    decision_comment: Mapped[str] = mapped_column(Text, default="")
    decided_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
