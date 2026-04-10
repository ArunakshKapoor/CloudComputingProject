from sqlalchemy.orm import Session
from app.db.models.memory import Memory


class MemoryRepository:
    def __init__(self, db: Session):
        self.db=db

    def by_user(self, user_id: str):
        return self.db.query(Memory).filter(Memory.user_id==user_id).all()
