from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.workflow import Base


class PolicyRule(Base):
    __tablename__ = "policy_rules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    action_type: Mapped[str] = mapped_column(String, unique=True)
    risk_level: Mapped[str] = mapped_column(String)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=False)
    allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    reason_template: Mapped[str] = mapped_column(String)
