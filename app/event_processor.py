from sqlalchemy.orm import Session
from . import models, schemas
from .state_machine import StateMachine
from datetime import datetime

state_machine = StateMachine()

def process_event(db: Session, event: schemas.EventCreate):
    # 1. Create Event Record using new model names
    db_event = models.EPCEvent(
        epc=event.epc,
        event_type=event.event_type,
        location=event.location,
        timestamp=datetime.utcnow()
    )
    db.add(db_event)
    
    # 2. Update Tag State using new model names
    tag_state = db.query(models.EPCState).filter(models.EPCState.epc == event.epc).first()
    if not tag_state:
        tag_state = models.EPCState(epc=event.epc, current_state="UNKNOWN", location=event.location)
        db.add(tag_state)
    
    new_state = state_machine.transition(tag_state.current_state, event.event_type)
    tag_state.current_state = new_state
    tag_state.location = event.location
    tag_state.last_updated = datetime.utcnow()
    
    db.commit()
    db.refresh(db_event)
    return db_event
