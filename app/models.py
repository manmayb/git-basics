from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class EPCEvent(Base):
    __tablename__ = "epc_events"

    id = Column(Integer, primary_key=True)
    epc = Column(String, index=True)
    event_type = Column(String)
    location = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class EPCState(Base):
    __tablename__ = "epc_state"

    epc = Column(String, primary_key=True)
    current_state = Column(String)
    location = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)
