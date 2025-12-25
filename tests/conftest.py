import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import core.database as database
from api.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    with test_engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS raw_assets (
                id TEXT PRIMARY KEY,
                data TEXT
            );
        """))
    yield


@pytest.fixture(scope="function")
def db_session(monkeypatch):
    # 1. Override engine everywhere
    monkeypatch.setattr(database, "engine", test_engine)
    monkeypatch.setattr("api.routes.engine", test_engine)

    # 2. 🔥 Rebind SessionLocal (CRITICAL)
    monkeypatch.setattr(database, "SessionLocal", TestingSessionLocal)
    monkeypatch.setattr(
    "services.etl_service.database.SessionLocal",
    TestingSessionLocal
    )
    with test_engine.begin() as conn:
        conn.execute(text("DELETE FROM raw_assets"))
    yield

@pytest.fixture(scope="function")
def client(db_session):
    return TestClient(app)
