# from schemas.unified import UnifiedAsset
# from core.database import SessionLocal
# from core.logging import logger
# import uuid, time

# def process_records(source, records):
#     db = SessionLocal()
#     run_id = str(uuid.uuid4())
#     start = time.time()

#     for r in records:
#         try:
#             asset = UnifiedAsset(
#                 asset_id=str(r.get("id")),
#                 name=r.get("name"),
#                 symbol=r.get("symbol"),
#                 price_usd=float(r.get("price_usd", r.get("current_price", 0))),
#                 source=source
#             )
#             db.execute(
#                 "INSERT INTO raw_assets VALUES (:id,:data)",
#                 {"id": asset.asset_id, "data": asset.json()}
#             )
#         except Exception as e:
#             logger.error(f"Schema error: {e}")

#     db.commit()
#     logger.info(f"ETL run {run_id} finished in {time.time() - start}")
from schemas.unified import UnifiedAsset
import core.database as database

from core.logging import logger
from sqlalchemy import text
import json

import uuid, time
def extract_price_usd(source, record):
    if source == "coingecko":
        return float(record.get("current_price", 0))

    if source == "coinpaprika":
        return float(
            record.get("quotes", {})
                  .get("USD", {})
                  .get("price", 0)
        )

    return 0.0


# def process_records(source, records):
#     db = database.SessionLocal()

#     run_id = str(uuid.uuid4())
#     start = time.time()
#     processed = 0

#     try:
#         for r in records:
#             try:
#                 asset = UnifiedAsset(
#                     asset_id=str(r.get("id")),
#                     name=r.get("name"),
#                     symbol=r.get("symbol"),
#                     price_usd=extract_price_usd(source, r),
#                     source=source
#                 )


#                 db.execute(
#                     text("""
#                         INSERT INTO raw_assets (id, data)
#                         VALUES (:id, :data)
#                         ON CONFLICT (id) DO NOTHING
#                     """),
#                     {
#                         "id": asset.asset_id,
#                         "data": json.dumps(asset.model_dump())
#                     }
#                 )

#                 processed += 1

#             except Exception as e:
#                 logger.error(f"Schema error: {e}")

#         db.commit()

#     except Exception as e:
#         db.rollback()
#         logger.error(f"ETL run failed: {e}")

#     finally:
#         db.close()

#     logger.info(
#         f"ETL run {run_id} | source={source} | "
#         f"records={processed} | "
#         f"duration={round(time.time() - start, 2)}s"
#     )
def process_records(source, records, db=None):
    external_db = db is not None
    db = db or database.SessionLocal()

    run_id = str(uuid.uuid4())
    start = time.time()
    processed = 0

    try:
        for r in records:
            try:
                asset = UnifiedAsset(
                    asset_id=str(r.get("id")),
                    name=r.get("name"),
                    symbol=r.get("symbol"),
                    price_usd=extract_price_usd(source, r),
                    source=source
                )

                db.execute(
                    text("""
                        INSERT INTO raw_assets (id, data)
                        VALUES (:id, :data)
                        ON CONFLICT (id) DO NOTHING
                    """),
                    {
                        "id": asset.asset_id,
                        "data": json.dumps(asset.dict())

                    }
                )

                processed += 1

            except Exception as e:
                logger.error(f"Schema error: {e}")

        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(f"ETL run failed: {e}")

    finally:
        if not external_db:
            db.close()

    logger.info(
        f"ETL run {run_id} | source={source} | "
        f"records={processed} | "
        f"duration={round(time.time() - start, 2)}s"
    )
