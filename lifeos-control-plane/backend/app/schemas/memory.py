from datetime import datetime
from pydantic import BaseModel


class MemoryCreateRequest(BaseModel):
    user_id: str
    key: str
    value: str
    source: str = "user"
    confidence: float = 0.8


class MemoryUpdateRequest(BaseModel):
    value: str
    confidence: float = 0.8


class MemoryOut(BaseModel):
    id: str
    user_id: str
    key: str
    value: str
    source: str
    confidence: float
    created_at: datetime
