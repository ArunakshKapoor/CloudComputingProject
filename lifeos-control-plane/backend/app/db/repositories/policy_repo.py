from sqlalchemy.orm import Session
from app.db.models.policy import PolicyRule


class PolicyRepository:
    def __init__(self, db: Session):
        self.db=db

    def list(self):
        return self.db.query(PolicyRule).all()
