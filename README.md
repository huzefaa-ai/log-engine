# 🚀 Distributed Log Engine

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![Celery](https://img.shields.io/badge/Celery-Async-green.svg)
![Redis](https://img.shields.io/badge/Redis-Broker-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)

A high-performance, asynchronous log ingestion and search system engineered with **FastAPI**, **Celery**, **Redis**, and **PostgreSQL**. Built to handle decoupled task processing and fast log indexing in containerized environments.

---

## 🏗️ Architecture & Data Flow

```mermaid
flowchart LR
    Client[Client / Application] -->|1. POST /api/v1/logs| API[FastAPI Gateway]
    API -->|2. Dispatch Task| Redis[(Redis Broker)]
    Redis -->|3. Consume Task| Worker[Celery Worker]
    Worker -->|4. Persist Log| DB[(PostgreSQL DB)]
    Client -->|5. GET /api/v1/search| API
    API -->|6. Query Data| DB
```

* **FastAPI**: Handles HTTP endpoints for ingesting, querying, and searching logs.
* **Celery**: Processes log ingestion tasks asynchronously.
* **Redis**: Acts as the message broker for Celery task queues.
* **PostgreSQL**: Persists structured log data with UUID primary keys.
* **Docker Compose**: Orchestrates all services into containerized environments.

---

## Quick Start

### 1. Run the Application

Start all services in detached mode:
```bash
docker compose up -d --build
```

### 2. Verify System Health

Check that all containers are active:
```bash
docker compose ps
```

The API will be available at `http://localhost:8000`. You can also explore the interactive API docs at `http://localhost:8000/docs`.

### 3. API Usage Examples

**Ingest a Log (Asynchronous)**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/logs" -Method Post -ContentType "application/json" -Body '{"message": "System test", "level": "INFO"}'
```

**Search Logs**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/search?q=System" -Method Get
```

### 4. Shutdown

To stop and remove containers:
```bash
docker compose down
```
