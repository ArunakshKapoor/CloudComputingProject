from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models.trace import TraceEvent
from app.dependencies import get_db
from app.schemas.trace import TraceEventOut

router = APIRouter(tags=["trace"])


@router.get("/workflows/{workflow_id}/trace", response_model=list[TraceEventOut])
def workflow_trace(workflow_id: str, db: Session = Depends(get_db)):
    rows = db.query(TraceEvent).filter(TraceEvent.workflow_id == workflow_id).order_by(TraceEvent.timestamp.asc()).all()
    return [TraceEventOut(id=r.id, stage=r.stage, event_type=r.event_type, message=r.message, metadata_json=r.metadata_json, timestamp=r.timestamp) for r in rows]
