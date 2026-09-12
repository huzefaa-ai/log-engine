from fastapi import FastAPI, BackgroundTasks, Query
from pydantic import BaseModel
from app.indexer import engine

app = FastAPI(title="Distributed Log Collector & Search Engine")

class LogPayload(BaseModel):
    level: str
    service: str
    message: str

def process_log(level: str, service: str, message: str):
    engine.add_log(level, service, message)

@app.post("/api/v1/logs", status_code=202)
async def ingest_log(payload: LogPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_log, payload.level, payload.service, payload.message)
    return {"status": "queued", "message": "Log received for processing"}

@app.get("/api/v1/search")
async def search_logs(q: str = Query(..., description="Keyword query to search in logs")):
    results = engine.search(q)
    return {"query": q, "total_matches": len(results), "results": results}