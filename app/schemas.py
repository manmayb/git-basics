from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class EventCreate(BaseModel):
    epc: str
    event_type: str
    location: str

class Event(BaseModel):
    id: int
    epc: str
    event_type: str
    location: str
    timestamp: datetime

    class Config:
        from_attributes = True

class TagState(BaseModel):
    epc: str
    current_state: str
    location: str
    last_updated: datetime

    class Config:
        from_attributes = True
        