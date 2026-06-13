from enum import StrEnum

from pydantic import BaseModel, Field

from app.models.backtest import Candle


class MarketDataProviderName(StrEnum):
    fixture = "fixture"
    indexer = "indexer"
    dexscreener = "dexscreener"


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


class PairQuery(BaseModel):
    chain_slug: str = Field(..., min_length=1, examples=["ethereum"])
    pair_address: str = Field(
        ...,
        min_length=1,
        examples=["0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"],
    )


class TokenInfo(BaseModel):
    address: str | None = None
    name: str | None = None
    symbol: str | None = None


class PairLiquidity(BaseModel):
    usd: float | None = None
    base: float | None = None
    quote: float | None = None


class PairTransactions(BaseModel):
    buys: int = 0
    sells: int = 0


class PairMarketData(BaseModel):
    provider: MarketDataProviderName = MarketDataProviderName.dexscreener
    chain_slug: str
    dex_id: str | None = None
    pair_address: str
    url: str | None = None
    base_token: TokenInfo
    quote_token: TokenInfo
    price_native: float | None = None
    price_usd: float | None = None
    liquidity: PairLiquidity | None = None
    volume: dict[str, float] = Field(default_factory=dict)
    price_change: dict[str, float] = Field(default_factory=dict)
    txns: dict[str, PairTransactions] = Field(default_factory=dict)
    fdv: float | None = None
    market_cap: float | None = None
    pair_created_at: int | None = None
