from pydantic import BaseModel, Field


class ChainStatus(BaseModel):
    name: str
    chain_id: int
    rpc_url: str
    latest_block: int
    explorer_url: str
    currency_symbol: str


class NativeBalanceRequest(BaseModel):
    address: str = Field(..., min_length=1, examples=["0x0000000000000000000000000000000000000000"])


class NativeBalanceResponse(BaseModel):
    chain_id: int
    address: str
    balance_wei: int
    balance_native: float
    currency_symbol: str
    explorer_url: str
