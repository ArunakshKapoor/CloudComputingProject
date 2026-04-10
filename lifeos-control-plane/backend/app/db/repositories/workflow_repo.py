from sqlalchemy.orm import Session

from app.db.models.workflow import WorkflowRun, WorkflowStep


class WorkflowRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[WorkflowRun]:
        return self.db.query(WorkflowRun).order_by(WorkflowRun.created_at.desc()).all()
