# Distributed Log Engine

A high-performance, asynchronous log ingestion and search system built with FastAPI, Celery, Redis, and PostgreSQL.

## Architecture

```mermaid
flowchart LR
    A[Client / HTTP Request] -->|POST /api/v1/logs| B(FastAPI API Gateway)
    B -->|Push Task| C[(Redis Broker)]
    C -->|Worker Fetch| D[Celery Async Workers]
    D -->|Persist Log| E[(PostgreSQL Database)]
