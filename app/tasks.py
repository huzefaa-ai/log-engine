import uuid
from app.celery_app import celery_app
from app.db import SessionLocal, LogModel

@celery_app.task
def ingest_log_task(log_id: str, message: str, level: str):
    db = SessionLocal()
    try:
        log_entry = LogModel(
            id=log_id,
            message=message,
            level=level.upper()
        )
        db.add(log_entry)
        db.commit()
        return log_entry.id
    finally:
        db.close()