from fastapi import APIRouter, HTTPException, status

from app.models.market_data import CandleQuery, CandleResponse
from app.services.market_data import provider_for_query

router = APIRouter()


@router.post("/candles", response_model=CandleResponse)
def get_candles(payload: CandleQuery) -> CandleResponse:
    try:
        return provider_for_query(payload).get_candles(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
