from typing import Protocol

import httpx

from app.core.config import settings
from app.models.backtest import Candle
from app.models.market_data import (
    CandleQuery,
    CandleResponse,
    MarketDataProviderName,
    PairLiquidity,
    PairMarketData,
    PairQuery,
    PairTransactions,
    TokenInfo,
)


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


class DexScreenerProvider:
    base_url = "https://api.dexscreener.com"

    def __init__(self, client: httpx.Client | None = None) -> None:
        self.client = client or httpx.Client(timeout=10)

    def get_pair(self, query: PairQuery) -> PairMarketData:
        response = self.client.get(
            f"{self.base_url}/latest/dex/pairs/{query.chain_slug}/{query.pair_address}"
        )
        response.raise_for_status()
        payload = response.json()
        pairs = payload.get("pairs") or []
        if not pairs:
            raise ValueError("DexScreener returned no pair data for the requested pair")
        return self._map_pair(pairs[0])

    @classmethod
    def _map_pair(cls, pair: dict) -> PairMarketData:
        return PairMarketData(
            chain_slug=str(pair.get("chainId") or ""),
            dex_id=pair.get("dexId"),
            pair_address=str(pair.get("pairAddress") or ""),
            url=pair.get("url"),
            base_token=TokenInfo.model_validate(pair.get("baseToken") or {}),
            quote_token=TokenInfo.model_validate(pair.get("quoteToken") or {}),
            price_native=cls._float_or_none(pair.get("priceNative")),
            price_usd=cls._float_or_none(pair.get("priceUsd")),
            liquidity=PairLiquidity.model_validate(pair.get("liquidity") or {}),
            volume=cls._float_map(pair.get("volume") or {}),
            price_change=cls._float_map(pair.get("priceChange") or {}),
            txns={
                key: PairTransactions.model_validate(value)
                for key, value in (pair.get("txns") or {}).items()
            },
            fdv=cls._float_or_none(pair.get("fdv")),
            market_cap=cls._float_or_none(pair.get("marketCap")),
            pair_created_at=pair.get("pairCreatedAt"),
        )

    @staticmethod
    def _float_or_none(value: object) -> float | None:
        if value is None:
            return None
        return float(value)

    @classmethod
    def _float_map(cls, values: dict[str, object]) -> dict[str, float]:
        return {
            key: parsed
            for key, value in values.items()
            if (parsed := cls._float_or_none(value)) is not None
        }
