from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models.memory import Memory
from app.dependencies import get_db
from app.schemas.memory import MemoryCreateRequest, MemoryOut, MemoryUpdateRequest

router = APIRouter(prefix="/memory", tags=["memory"])


@router.get("", response_model=list[MemoryOut])
def list_memory(user_id: str, db: Session = Depends(get_db)):
    rows = db.query(Memory).filter(Memory.user_id == user_id).all()
    return [MemoryOut(id=r.id, user_id=r.user_id, key=r.key, value=r.value, source=r.source, confidence=r.confidence, created_at=r.created_at) for r in rows]


@router.post("", response_model=MemoryOut)
def create_memory(payload: MemoryCreateRequest, db: Session = Depends(get_db)):
    m = Memory(id=str(uuid4()), **payload.model_dump())
    db.add(m)
    db.commit()
    return MemoryOut(id=m.id, user_id=m.user_id, key=m.key, value=m.value, source=m.source, confidence=m.confidence, created_at=m.created_at)


@router.patch("/{memory_id}", response_model=MemoryOut)
def update_memory(memory_id: str, payload: MemoryUpdateRequest, db: Session = Depends(get_db)):
    m = db.get(Memory, memory_id)
    if not m:
        raise HTTPException(404, "memory not found")
    m.value = payload.value
    m.confidence = payload.confidence
    db.commit()
    return MemoryOut(id=m.id, user_id=m.user_id, key=m.key, value=m.value, source=m.source, confidence=m.confidence, created_at=m.created_at)


@router.delete("/{memory_id}")
def delete_memory(memory_id: str, db: Session = Depends(get_db)):
    m = db.get(Memory, memory_id)
    if not m:
        raise HTTPException(404, "memory not found")
    db.delete(m)
    db.commit()
    return {"status": "ok"}
