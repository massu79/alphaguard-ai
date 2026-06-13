from typing import Protocol

import httpx

from app.core.config import settings
from app.models.backtest import Candle
from app.models.market_data import CandleQuery, CandleResponse, MarketDataProviderName


class MarketDataProvider(Protocol):
    provider_name: MarketDataProviderName

    def get_candles(self, query: CandleQuery) -> CandleResponse:
        """Return normalized candles for a pool or pair."""


class FixtureMarketDataProvider:
    provider_name = MarketDataProviderName.fixture

    def get_candles(self, query: CandleQuery) -> CandleResponse:
        closes = [10, 9, 8, 12, 14, 13, 11, 9]
        candles = [
            Candle(
                timestamp=index + 1,
                open=close,
                high=close,
                low=close,
                close=close,
                volume=1_000 + index,
                block_number=1_000_000 + index,
            )
            for index, close in enumerate(closes[: query.limit])
        ]
        return self._response(query, candles)

    def _response(self, query: CandleQuery, candles: list[Candle]) -> CandleResponse:
        return CandleResponse(
            chain_id=query.chain_id,
            pool_address=query.pool_address,
            asset=query.asset,
            interval=query.interval,
            provider=self.provider_name,
            candles=candles,
        )


class IndexerMarketDataProvider:
    provider_name = MarketDataProviderName.indexer

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.client = client or httpx.Client(timeout=10)

    def get_candles(self, query: CandleQuery) -> CandleResponse:
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None
        response = self.client.get(
            f"{self.base_url}/candles",
            params={
                "chain_id": query.chain_id,
                "pool_address": query.pool_address,
                "asset": query.asset,
                "interval": query.interval,
                "limit": query.limit,
            },
            headers=headers,
        )
        response.raise_for_status()
        payload = response.json()
        candles = [Candle.model_validate(item) for item in payload.get("candles", payload)]
        return CandleResponse(
            chain_id=query.chain_id,
            pool_address=query.pool_address,
            asset=query.asset,
            interval=query.interval,
            provider=self.provider_name,
            candles=candles,
        )


def provider_for_query(query: CandleQuery) -> MarketDataProvider:
    provider_name = query.provider or MarketDataProviderName(settings.market_data_provider)
    if provider_name == MarketDataProviderName.fixture:
        return FixtureMarketDataProvider()
    if not settings.market_data_base_url:
        raise ValueError("ALPHAGUARD_MARKET_DATA_BASE_URL is required for indexer provider")
    return IndexerMarketDataProvider(
        base_url=settings.market_data_base_url,
        api_key=settings.market_data_api_key,
    )
