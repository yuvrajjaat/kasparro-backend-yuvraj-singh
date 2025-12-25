from sqlalchemy import text
import core.database as database
from services.etl_service import process_records


def test_idempotent_ingestion(db_session):
    records = [
        {
            "id": "eth-ethereum",
            "name": "Ethereum",
            "symbol": "ETH",
            "price_usd": 2000
        }
    ]

    db = database.SessionLocal()

    process_records("coinpaprika", records, db=db)
    process_records("coinpaprika", records, db=db)

    result = db.execute(text("SELECT COUNT(*) FROM raw_assets")).scalar()
    db.close()

    assert result == 1
