from ingestion.coinpaprika import CoinPaprikaIngestor
from ingestion.coingecko import CoinGeckoIngestor
from ingestion.csv_source import CSVIngestor
from services.etl_service import process_records

def run_etl():
    sources = [
        ("coinpaprika", CoinPaprikaIngestor()),
        ("coingecko", CoinGeckoIngestor()),
        ("csv", CSVIngestor())
    ]

    for name, src in sources:
        data = src.fetch()
        process_records(name, data)
