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


def test_dexscreener_pair_endpoint_returns_live_pair_shape() -> None:
    from app.api.v1.endpoints import market_data
    from app.models.market_data import PairMarketData, TokenInfo

    class FakeDexScreenerProvider:
        def get_pair(self, query):
            return PairMarketData(
                chain_slug=query.chain_slug,
                dex_id="uniswap",
                pair_address=query.pair_address,
                base_token=TokenInfo(symbol="WETH"),
                quote_token=TokenInfo(symbol="USDC"),
                price_usd=3500.25,
            )

    market_data.DexScreenerProvider = FakeDexScreenerProvider

    response = client.post(
        "/api/v1/market-data/pair",
        json={
            "chain_slug": "ethereum",
            "pair_address": "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "dexscreener"
    assert payload["chain_slug"] == "ethereum"
    assert payload["pair_address"]
    assert payload["base_token"]["symbol"]
    assert payload["quote_token"]["symbol"]


def test_dexscreener_provider_maps_pair_response() -> None:
    from app.models.market_data import PairQuery
    from app.services.market_data import DexScreenerProvider

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith(
            "/latest/dex/pairs/ethereum/0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"
        )
        return httpx.Response(
            200,
            json={
                "pairs": [
                    {
                        "chainId": "ethereum",
                        "dexId": "uniswap",
                        "url": "https://dexscreener.com/ethereum/pair",
                        "pairAddress": "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",
                        "baseToken": {
                            "address": "0xbase",
                            "name": "Wrapped Ether",
                            "symbol": "WETH",
                        },
                        "quoteToken": {"address": "0xquote", "name": "USD Coin", "symbol": "USDC"},
                        "priceNative": "1",
                        "priceUsd": "3500.25",
                        "txns": {"h24": {"buys": 10, "sells": 8}},
                        "volume": {"h24": 123456.78},
                        "priceChange": {"h24": 1.25},
                        "liquidity": {"usd": 987654.32, "base": 100, "quote": 350000},
                        "fdv": 1000000,
                        "marketCap": 900000,
                        "pairCreatedAt": 1717200000000,
                    }
                ]
            },
        )

    provider = DexScreenerProvider(client=httpx.Client(transport=httpx.MockTransport(handler)))
    payload = provider.get_pair(
        PairQuery(
            chain_slug="ethereum",
            pair_address="0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",
        )
    )

    assert payload.provider == "dexscreener"
    assert payload.price_usd == 3500.25
    assert payload.liquidity
    assert payload.liquidity.usd == 987654.32
    assert payload.txns["h24"].buys == 10
