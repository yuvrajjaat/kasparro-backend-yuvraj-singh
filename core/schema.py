import time
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from core.database import engine

def wait_for_db(retries=10, delay=2):
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except OperationalError:
            print(f"⏳ Waiting for DB... ({i+1}/{retries})")
            time.sleep(delay)
    raise RuntimeError("❌ Database not available after retries")

def init_schema():
    wait_for_db()

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS raw_assets (
                id TEXT PRIMARY KEY,
                data JSONB NOT NULL
            );
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS etl_runs (
                run_id UUID PRIMARY KEY,
                source TEXT,
                started_at TIMESTAMP,
                finished_at TIMESTAMP,
                status TEXT,
                records_processed INT
            );
        """))

    print("✅ Database schema initialized")
