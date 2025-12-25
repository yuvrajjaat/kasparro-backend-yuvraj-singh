from services.etl_service import process_records


def test_price_extraction_coingecko():
    records = [
        {
            "id": "bitcoin",
            "name": "Bitcoin",
            "symbol": "btc",
            "current_price": 100.5
        }
    ]

    process_records("coingecko", records)

def test_price_extraction_coinpaprika():
    records = [
        {
            "id": "btc-bitcoin",
            "name": "Bitcoin",
            "symbol": "BTC",
            "price_usd": 101.2
        }
    ]

    process_records("coinpaprika", records)
