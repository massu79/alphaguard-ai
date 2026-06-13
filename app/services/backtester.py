from app.models.backtest import (
    BacktestMetrics,
    BacktestRequest,
    BacktestResponse,
    BacktestTrade,
    Candle,
    TradeAction,
)
from app.services.onchain_data import InlineOnChainDataProvider, OnChainMarketDataProvider


class MovingAverageBacktester:
    def __init__(self, market_data_provider: OnChainMarketDataProvider | None = None) -> None:
        self.market_data_provider = market_data_provider or InlineOnChainDataProvider()

    def run(self, request: BacktestRequest) -> BacktestResponse:
        candles = self.market_data_provider.get_candles(request)
        cash = request.initial_cash
        position = 0.0
        trades: list[BacktestTrade] = []
        equity_curve: list[float] = []

        for index, candle in enumerate(candles):
            price = candle.close
            equity_curve.append(cash + position * price)

            if index < request.long_window:
                continue

            previous_short = self._average_close(
                candles[index - request.short_window : index]
            )
            previous_long = self._average_close(candles[index - request.long_window : index])
            current_short = self._average_close(
                candles[index - request.short_window + 1 : index + 1]
            )
            current_long = self._average_close(
                candles[index - request.long_window + 1 : index + 1]
            )

            if position == 0 and previous_short <= previous_long and current_short > current_long:
                fee = cash * request.trading_fee_bps / 10_000
                quantity = (cash - fee) / price
                position = quantity
                cash = 0.0
                trades.append(
                    self._trade(candle, TradeAction.buy, quantity, fee, cash, position)
                )
            elif position > 0 and previous_short >= previous_long and current_short < current_long:
                gross = position * price
                fee = gross * request.trading_fee_bps / 10_000
                cash = gross - fee
                quantity = position
                position = 0.0
                trades.append(
                    self._trade(candle, TradeAction.sell, quantity, fee, cash, position)
                )

        ending_equity = cash + position * candles[-1].close
        equity_curve.append(ending_equity)
        metrics = self._metrics(request.initial_cash, ending_equity, equity_curve, trades)

        return BacktestResponse(
            chain_id=request.chain_id,
            asset=request.asset,
            strategy=request.strategy,
            initial_cash=request.initial_cash,
            candles_processed=len(candles),
            metrics=metrics,
            trades=trades,
        )

    @staticmethod
    def _average_close(candles: list[Candle]) -> float:
        return sum(candle.close for candle in candles) / len(candles)

    @staticmethod
    def _trade(
        candle: Candle,
        action: TradeAction,
        quantity: float,
        fee: float,
        cash_after: float,
        position_after: float,
    ) -> BacktestTrade:
        return BacktestTrade(
            timestamp=candle.timestamp,
            action=action,
            price=candle.close,
            quantity=round(quantity, 8),
            fee=round(fee, 8),
            cash_after=round(cash_after, 8),
            position_after=round(position_after, 8),
        )

    @staticmethod
    def _metrics(
        initial_cash: float,
        ending_equity: float,
        equity_curve: list[float],
        trades: list[BacktestTrade],
    ) -> BacktestMetrics:
        max_equity = equity_curve[0]
        max_drawdown = 0.0

        for equity in equity_curve:
            max_equity = max(max_equity, equity)
            if max_equity:
                drawdown = (max_equity - equity) / max_equity
                max_drawdown = max(max_drawdown, drawdown)

        return BacktestMetrics(
            ending_equity=round(ending_equity, 4),
            total_return_pct=round((ending_equity - initial_cash) / initial_cash * 100, 4),
            max_drawdown_pct=round(max_drawdown * 100, 4),
            trades_count=len(trades),
        )
