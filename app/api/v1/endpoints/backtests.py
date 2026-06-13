from fastapi import APIRouter

from app.models.backtest import BacktestRequest, BacktestResponse
from app.services.backtester import MovingAverageBacktester

router = APIRouter()
backtester = MovingAverageBacktester()


@router.post("/run", response_model=BacktestResponse)
def run_backtest(payload: BacktestRequest) -> BacktestResponse:
    return backtester.run(payload)
