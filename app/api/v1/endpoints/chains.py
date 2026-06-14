import httpx
from fastapi import APIRouter, HTTPException, status

from app.models.chains import ChainStatus, NativeBalanceRequest, NativeBalanceResponse
from app.services.chains import JsonRpcError, MantleSepoliaClient

router = APIRouter()


@router.get("/mantle-sepolia/status", response_model=ChainStatus)
def mantle_sepolia_status() -> ChainStatus:
    try:
        return MantleSepoliaClient().status()
    except (JsonRpcError, httpx.HTTPError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Mantle Sepolia RPC request failed: {exc}",
        ) from exc


@router.post("/mantle-sepolia/balance", response_model=NativeBalanceResponse)
def mantle_sepolia_balance(payload: NativeBalanceRequest) -> NativeBalanceResponse:
    try:
        return MantleSepoliaClient().native_balance(payload.address)
    except (JsonRpcError, httpx.HTTPError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Mantle Sepolia RPC request failed: {exc}",
        ) from exc
