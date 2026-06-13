from typing import Protocol

from app.models.backtest import BacktestRequest, Candle


class OnChainMarketDataProvider(Protocol):
    def get_candles(self, request: BacktestRequest) -> list[Candle]:
        """Return normalized on-chain candle data for a backtest request."""


class InlineOnChainDataProvider:
    def get_candles(self, request: BacktestRequest) -> list[Candle]:
        return request.candles
