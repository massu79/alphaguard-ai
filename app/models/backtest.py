from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class StrategyName(StrEnum):
    moving_average_crossover = "moving_average_crossover"


class TradeAction(StrEnum):
    buy = "buy"
    sell = "sell"


class Candle(BaseModel):
    timestamp: int = Field(..., ge=0, examples=[1717200000])
    open: float = Field(..., gt=0, examples=[100.0])
    high: float = Field(..., gt=0, examples=[105.0])
    low: float = Field(..., gt=0, examples=[98.0])
    close: float = Field(..., gt=0, examples=[104.0])
    volume: float = Field(default=0, ge=0, examples=[12345.67])
    block_number: int | None = Field(default=None, ge=0, examples=[12345678])

    @model_validator(mode="after")
    def validate_price_range(self) -> "Candle":
        if self.high < max(self.open, self.close, self.low):
            raise ValueError("high must be greater than or equal to open, close, and low")
        if self.low > min(self.open, self.close, self.high):
            raise ValueError("low must be less than or equal to open, close, and high")
        return self


class BacktestRequest(BaseModel):
    chain_id: int = Field(..., ge=1, examples=[11155111])
    asset: str = Field(..., min_length=1, examples=["WETH/USDC"])
    strategy: StrategyName = StrategyName.moving_average_crossover
    initial_cash: float = Field(default=10_000, gt=0)
    short_window: int = Field(default=3, ge=1)
    long_window: int = Field(default=5, ge=2)
    trading_fee_bps: float = Field(default=0, ge=0, le=1_000)
    candles: list[Candle] = Field(..., min_length=2)

    @model_validator(mode="after")
    def validate_strategy_windows(self) -> "BacktestRequest":
        if self.short_window >= self.long_window:
            raise ValueError("short_window must be less than long_window")
        if len(self.candles) < self.long_window + 1:
            raise ValueError("candles must contain at least long_window + 1 records")
        return self


class BacktestTrade(BaseModel):
    timestamp: int
    action: TradeAction
    price: float
    quantity: float
    fee: float
    cash_after: float
    position_after: float


class BacktestMetrics(BaseModel):
    ending_equity: float
    total_return_pct: float
    max_drawdown_pct: float
    trades_count: int


class BacktestResponse(BaseModel):
    chain_id: int
    asset: str
    strategy: StrategyName
    initial_cash: float
    candles_processed: int
    metrics: BacktestMetrics
    trades: list[BacktestTrade]
    mode: str = "backtest"
