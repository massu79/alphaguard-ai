from enum import StrEnum

from pydantic import BaseModel, Field

from app.models.backtest import Candle


class MarketDataProviderName(StrEnum):
    fixture = "fixture"
    indexer = "indexer"


class CandleInterval(StrEnum):
    one_minute = "1m"
    five_minutes = "5m"
    fifteen_minutes = "15m"
    one_hour = "1h"
    one_day = "1d"


class CandleQuery(BaseModel):
    chain_id: int = Field(..., ge=1, examples=[11155111])
    pool_address: str = Field(..., min_length=1, examples=["0xpool"])
    asset: str = Field(..., min_length=1, examples=["WETH/USDC"])
    interval: CandleInterval = CandleInterval.one_hour
    limit: int = Field(default=100, ge=2, le=1_000)
    provider: MarketDataProviderName | None = None


class CandleResponse(BaseModel):
    chain_id: int
    pool_address: str
    asset: str
    interval: CandleInterval
    provider: MarketDataProviderName
    candles: list[Candle]
