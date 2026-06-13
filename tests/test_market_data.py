import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.models.market_data import CandleQuery
from app.services.market_data import IndexerMarketDataProvider

client = TestClient(app)


def test_get_fixture_candles_returns_normalized_market_data() -> None:
    response = client.post(
        "/api/v1/market-data/candles",
        json={
            "chain_id": 11155111,
            "pool_address": "0xpool",
            "asset": "WETH/USDC",
            "interval": "1h",
            "limit": 4,
            "provider": "fixture",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "fixture"
    assert payload["chain_id"] == 11155111
    assert len(payload["candles"]) == 4
    assert payload["candles"][0]["block_number"] == 1000000


def test_indexer_provider_maps_normalized_http_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/candles"
        assert request.url.params["chain_id"] == "11155111"
        assert request.headers["authorization"] == "Bearer test-key"
        return httpx.Response(
            200,
            json={
                "candles": [
                    {
                        "timestamp": 1717200000,
                        "open": 100,
                        "high": 110,
                        "low": 95,
                        "close": 105,
                        "volume": 1234,
                        "block_number": 12345678,
                    }
                ]
            },
        )

    provider = IndexerMarketDataProvider(
        base_url="https://indexer.example",
        api_key="test-key",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    query = CandleQuery(
        chain_id=11155111,
        pool_address="0xpool",
        asset="WETH/USDC",
        limit=10,
    )

    response = provider.get_candles(query)

    assert response.provider == "indexer"
    assert response.candles[0].close == 105
    assert response.candles[0].block_number == 12345678
