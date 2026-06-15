from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_renders_local_demo_page() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "AlphaGuard AI Demo" in response.text
    assert "MNT/USDT Paper-Trading Strategy Cockpit" in response.text
    assert "Trade Setup" in response.text
    assert "Start MNT/USDT Paper Trade" in response.text
    assert "Market Watch" in response.text
    assert "Current recommendation" in response.text
    assert "Active Position" in response.text
    assert "Unrealized PnL" in response.text
    assert "TP / SL" in response.text
    assert "Alpha Signal" in response.text
    assert "Strategy Audit Log" in response.text
    assert "Mantle Sepolia" in response.text
    assert "Paper Trading" in response.text
    assert "paperRows" in response.text
    assert "MNT/USDT" in response.text
    assert "TradingView real market chart" in response.text
    assert "realChartFrame" in response.text
    assert "Paper TP/SL overlay" in response.text
    assert "live forming candle" in response.text
    assert "Take profit %" in response.text
    assert "Stop loss %" in response.text
    assert "activePositionStrip" in response.text
    assert "priceChart" in response.text
    assert "Paper TP/SL overlay" in response.text
    assert "/api/v1/market-data/pair" in response.text
    assert "/api/v1/backtests/run" in response.text
