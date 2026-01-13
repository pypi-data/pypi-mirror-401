from datetime import datetime
from pydantic import BaseModel, Field
import uuid

class LogEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    tags: list[str] = []