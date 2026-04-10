from datetime import datetime
from pydantic import BaseModel


class TraceEventOut(BaseModel):
    id: int
    stage: str
    event_type: str
    message: str
    metadata_json: str
    timestamp: datetime
