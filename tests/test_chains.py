import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.services.chains import MantleSepoliaClient

client = TestClient(app)


def test_mantle_sepolia_client_maps_status_and_balance() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        payload = request.read().decode()
        if "eth_chainId" in payload:
            return httpx.Response(200, json={"jsonrpc": "2.0", "id": 1, "result": "0x138b"})
        if "eth_blockNumber" in payload:
            return httpx.Response(200, json={"jsonrpc": "2.0", "id": 1, "result": "0x10"})
        if "eth_getBalance" in payload:
            return httpx.Response(
                200,
                json={"jsonrpc": "2.0", "id": 1, "result": "0xde0b6b3a7640000"},
            )
        return httpx.Response(400)

    rpc = MantleSepoliaClient(
        rpc_url="https://rpc.example",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    status = rpc.status()
    balance = rpc.native_balance("0x0000000000000000000000000000000000000000")

    assert status.chain_id == 5003
    assert status.latest_block == 16
    assert balance.balance_native == 1
    assert balance.currency_symbol == "MNT"


def test_mantle_status_endpoint_shape() -> None:
    response = client.get("/api/v1/chains/mantle-sepolia/status")

    assert response.status_code in {200, 503}
    if response.status_code == 200:
        assert response.json()["chain_id"] == 5003
