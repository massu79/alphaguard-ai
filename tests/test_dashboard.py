from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_renders_local_demo_page() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "AlphaGuard AI Demo" in response.text
    assert "Market Watch" in response.text
    assert "Mantle Sepolia" in response.text
    assert "Paper Trading" in response.text
    assert "paperRows" in response.text
    assert "MNT/USDT" in response.text
    assert "live forming candle" in response.text
    assert "Take profit %" in response.text
    assert "Stop loss %" in response.text
    assert "activePositionStrip" in response.text
    assert "priceChart" in response.text
    assert "Candles + volume" in response.text
    assert "/api/v1/market-data/pair" in response.text
    assert "/api/v1/backtests/run" in response.text
