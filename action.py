from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActionRequest(BaseModel):
    current_action: str

class ActionSequence(BaseModel):
    current_action: str
    next_action: str
    confidence: float

class ActionTrackRequest(BaseModel):
    action_name: str
    user_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[dict] = None