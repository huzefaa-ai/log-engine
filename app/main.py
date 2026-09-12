from fastapi import FastAPI, Query, HTTPException
from app.db import SessionLocal, LogModel
from app.tasks import process_log_task

app = FastAPI(title="Distributed Logging System")

@app.post("/api/v1/logs", status_code=202)
def create_log(payload: dict):
    task = process_log_task.delay(payload)
    return {
        "status": "queued",
        "task_id": task.id,
        "message": "Log entry processing initiated"
    }

@app.get("/api/v1/search")
def search_logs(q: str = Query(None), level: str = Query(None)):
    db = SessionLocal()
    try:
        query = db.query(LogModel)
        if q:
            query = query.filter(LogModel.message.ilike(f"%{q}%"))
        if level:
            query = query.filter(LogModel.level == level.upper())

        results = query.all()
        return {
            "count": len(results),
            "results": [
                {
                    "id": log.id,
                    "message": log.message,
                    "level": log.level,
                    "timestamp": log.timestamp.isoformat()
                } for log in results
            ]
        }
    finally:
        db.close()

@app.get("/api/v1/logs/{log_id}")
def get_log(log_id: str):
    db = SessionLocal()
    try:
        log_entry = db.query(LogModel).filter(LogModel.id == log_id).first()
        if not log_entry:
            raise HTTPException(status_code=404, detail="Log entry not found")
        
        return {
            "id": log_entry.id,
            "message": log_entry.message,
            "level": log_entry.level,
            "timestamp": log_entry.timestamp.isoformat()
        }
    finally:
        db.close()