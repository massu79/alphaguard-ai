from typing import Any

import httpx

from app.core.config import settings
from app.models.chains import ChainStatus, NativeBalanceResponse


class JsonRpcError(RuntimeError):
    pass


class MantleSepoliaClient:
    name = "Mantle Sepolia"
    chain_id = 5003
    explorer_url = "https://explorer.sepolia.mantle.xyz"
    currency_symbol = "MNT"

    def __init__(self, rpc_url: str | None = None, client: httpx.Client | None = None) -> None:
        self.rpc_url = rpc_url or settings.mantle_sepolia_rpc_url
        self.client = client or httpx.Client(timeout=10)

    def status(self) -> ChainStatus:
        chain_id = int(self._rpc("eth_chainId", []), 16)
        latest_block = int(self._rpc("eth_blockNumber", []), 16)
        return ChainStatus(
            name=self.name,
            chain_id=chain_id,
            rpc_url=self.rpc_url,
            latest_block=latest_block,
            explorer_url=self.explorer_url,
            currency_symbol=self.currency_symbol,
        )

    def native_balance(self, address: str) -> NativeBalanceResponse:
        balance_wei = int(self._rpc("eth_getBalance", [address, "latest"]), 16)
        return NativeBalanceResponse(
            chain_id=self.chain_id,
            address=address,
            balance_wei=balance_wei,
            balance_native=round(balance_wei / 10**18, 8),
            currency_symbol=self.currency_symbol,
            explorer_url=f"{self.explorer_url}/address/{address}",
        )

    def _rpc(self, method: str, params: list[Any]) -> Any:
        response = self.client.post(
            self.rpc_url,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params,
            },
        )
        response.raise_for_status()
        payload = response.json()
        if "error" in payload:
            raise JsonRpcError(str(payload["error"]))
        return payload["result"]
