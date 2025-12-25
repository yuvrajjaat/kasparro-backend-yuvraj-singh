from fastapi import FastAPI
from api.routes import router
from core.schema import init_schema
from ingestion.runner import run_etl
import threading

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
def startup():
    init_schema()
    threading.Thread(target=run_etl, daemon=True).start()
