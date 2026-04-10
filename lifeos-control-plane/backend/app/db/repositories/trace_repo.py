from sqlalchemy.orm import Session
from app.db.models.trace import TraceEvent


class TraceRepository:
    def __init__(self, db: Session):
        self.db=db

    def by_workflow(self, workflow_id: str):
        return self.db.query(TraceEvent).filter(TraceEvent.workflow_id==workflow_id).order_by(TraceEvent.timestamp.asc()).all()
