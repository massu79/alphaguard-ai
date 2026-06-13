import httpx
from fastapi import APIRouter, HTTPException, status

from app.models.market_data import CandleQuery, CandleResponse, PairMarketData, PairQuery
from app.services.market_data import DexScreenerProvider, provider_for_query

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


@router.post("/pair", response_model=PairMarketData)
def get_pair(payload: PairQuery) -> PairMarketData:
    try:
        return DexScreenerProvider().get_pair(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"DexScreener request failed: {exc}",
        ) from exc
