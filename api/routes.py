from fastapi import APIRouter
from core.database import engine
from sqlalchemy import text
import time, uuid
import json
router = APIRouter()

@router.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"db": "ok", "etl": "running"}
    except Exception as e:
        return {"db": "down", "error": str(e)}

from ingestion.runner import run_etl

@router.post("/etl/run")
def run_etl_now():
    run_etl()
    return {"status": "etl triggered"}


@router.get("/data")
def data(limit: int = 10, offset: int = 0):
    start = time.time()

    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT data FROM raw_assets LIMIT :l OFFSET :o"),
            {"l": limit, "o": offset}
        ).fetchall()

    return {
        "request_id": str(uuid.uuid4()),
        "api_latency_ms": int((time.time() - start) * 1000),
        "data": [
            r[0] if isinstance(r[0], dict) else json.loads(r[0])
            for r in rows
        ]

    }

@router.get("/stats")
def stats():
    with engine.connect() as conn:
        count = conn.execute(
            text("SELECT COUNT(*) FROM raw_assets")
        ).fetchone()

    return {"count": count[0]}
