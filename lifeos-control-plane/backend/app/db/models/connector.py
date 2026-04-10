from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.workflow import Base


class ConnectorStatus(Base):
    __tablename__ = "connector_status"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    mode: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
