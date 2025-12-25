from services.etl_service import process_records


def test_api_data_endpoint(client):
    records = [
        {
            "id": "btc-bitcoin",
            "name": "Bitcoin",
            "symbol": "BTC",
            "price_usd": 50000
        }
    ]

    process_records("coinpaprika", records)

    response = client.get("/data?limit=10&offset=0")

    assert response.status_code == 200

    body = response.json()
    assert "data" in body
    assert len(body["data"]) == 1
    assert body["data"][0]["symbol"] == "BTC"
