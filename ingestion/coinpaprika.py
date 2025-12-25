import requests
from ingestion.base import BaseIngestor
from core.config import settings

class CoinPaprikaIngestor(BaseIngestor):
    def fetch(self):
        # headers = {"Authorization": f"Bearer {settings.COINPAPRIKA_API_KEY}"}
        r = requests.get(f"{settings.COINPAPRIKA_BASE_URL}/tickers")
        r.raise_for_status()
        return r.json()
