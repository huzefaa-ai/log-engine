import uuid
from app.celery_app import celery_app
from app.db import SessionLocal, LogModel

@celery_app.task
def process_log_task(payload: dict):
    db = SessionLocal()
    try:
        log_entry = LogModel(
            id=str(uuid.uuid4()),
            message=payload.get("message", ""),
            level=payload.get("level", "INFO").upper()
        )
        db.add(log_entry)
        db.commit()
        return log_entry.id
    finally:
        db.close()