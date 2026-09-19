import uuid
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.db import SessionLocal, LogModel
from app.tasks import ingest_log_task

app = FastAPI(title="Distributed Log Engine", version="1.0.0")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class LogCreate(BaseModel):
    message: str
    level: str = "INFO"

class LogResponse(BaseModel):
    id: str
    message: str
    level: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class SearchResponse(BaseModel):
    count: int
    results: List[LogResponse]

# Endpoints
@app.post("/api/v1/logs", status_code=status.HTTP_202_ACCEPTED)
def create_log(log_data: LogCreate):
    log_id = str(uuid.uuid4())
    ingest_log_task.delay(log_id, log_data.message, log_data.level)
    return {
        "status": "queued",
        "log_id": log_id,
        "message": "Log entry accepted for background processing."
    }

@app.get("/api/v1/logs/{log_id}", response_model=LogResponse)
def get_log(log_id: str, db: Session = Depends(get_db)):
    log_entry = db.query(LogModel).filter(LogModel.id == log_id).first()
    if not log_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Log with ID {log_id} not found."
        )
    return log_entry

@app.get("/api/v1/search", response_model=SearchResponse)
def search_logs(
    q: Optional[str] = Query(None, description="Search keyword in log message"),
    level: Optional[str] = Query(None, description="Filter by log level (e.g. INFO, ERROR)"),
    db: Session = Depends(get_db)
):
    query = db.query(LogModel)
    
    if q:
        query = query.filter(LogModel.message.ilike(f"%{q}%"))
    if level:
        query = query.filter(LogModel.level.ilike(level))
        
    results = query.order_by(LogModel.timestamp.desc()).all()
    return SearchResponse(count=len(results), results=results)