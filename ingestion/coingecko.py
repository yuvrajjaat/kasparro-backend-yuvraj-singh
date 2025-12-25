import requests
from ingestion.base import BaseIngestor
from core.config import settings

class CoinGeckoIngestor(BaseIngestor):
    def fetch(self):
        r = requests.get(f"{settings.COINGECKO_BASE_URL}/coins/markets",
                         params={"vs_currency": "usd"})
        r.raise_for_status()
        return r.json()
