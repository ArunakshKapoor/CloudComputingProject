from sqlalchemy.orm import Session
from app.db.models.approval import Approval


class ApprovalRepository:
    def __init__(self, db: Session):
        self.db=db

    def by_workflow(self, workflow_id: str):
        return self.db.query(Approval).filter(Approval.workflow_id==workflow_id).all()
