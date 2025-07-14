from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TextIn(BaseModel):
    text: str

class SummaryOut(BaseModel):
    summary: str

class SummaryRecord(BaseModel):
    id: Optional[str]  # MongoDB uses string IDs, not int
    text: str
    summary: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
