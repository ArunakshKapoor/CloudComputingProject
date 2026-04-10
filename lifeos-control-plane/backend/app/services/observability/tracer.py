import json
from app.db.models.trace import TraceEvent


def trace(db, workflow_id: str, stage: str, event_type: str, message: str, metadata: dict | None = None, step_id: str | None = None):
    evt = TraceEvent(workflow_id=workflow_id, step_id=step_id, stage=stage, event_type=event_type, message=message, metadata_json=json.dumps(metadata or {}))
    db.add(evt)
    db.commit()
