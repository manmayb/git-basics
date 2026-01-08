from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, event_processor
from .database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="RFID Simulator API")

@app.post("/rfid/event", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return event_processor.process_event(db, event)

@app.get("/tags/", response_model=List[schemas.TagState])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = db.query(models.EPCState).offset(skip).limit(limit).all()
    return tags

@app.get("/tags/{epc}", response_model=schemas.TagState)
def read_tag(epc: str, db: Session = Depends(get_db)):
    tag = db.query(models.EPCState).filter(models.EPCState.epc == epc).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag
     
