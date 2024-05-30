from django.test import TestCase


client = []


def test_create_ticker():
    response = client.post("/tickers/", json={"btcars": {"price": 1000000}})
    assert response.status_code == 200
    assert response.json() == {"message": "Ticker created"}


def test_get_price():
    timestamp = "2024-05-29T12:00:00"
    response = client.get(f"/tickers/price/?timestamp={timestamp}")
    assert response.status_code == 200


def test_get_average_price():
    response = client.get("/tickers/average_price/", json={"start_timestamp": "2024-05-28T00:00:00", "end_timestamp": "2024-05-29T00:00:00"})
    assert response.status_code == 200


def test_get_tickers():
    response = client.get("/tickers/")
    assert response.status_code == 200
