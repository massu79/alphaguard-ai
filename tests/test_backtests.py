from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_run_backtest_returns_demo_trade_log_and_metrics() -> None:
    response = client.post(
        "/api/v1/backtests/run",
        json={
            "chain_id": 11155111,
            "asset": "WETH/USDC",
            "initial_cash": 120,
            "short_window": 2,
            "long_window": 3,
            "candles": [
                {"timestamp": 1, "open": 10, "high": 10, "low": 10, "close": 10},
                {"timestamp": 2, "open": 9, "high": 9, "low": 9, "close": 9},
                {"timestamp": 3, "open": 8, "high": 8, "low": 8, "close": 8},
                {"timestamp": 4, "open": 12, "high": 12, "low": 12, "close": 12},
                {"timestamp": 5, "open": 14, "high": 14, "low": 14, "close": 14},
                {"timestamp": 6, "open": 13, "high": 13, "low": 13, "close": 13},
                {"timestamp": 7, "open": 11, "high": 11, "low": 11, "close": 11},
                {"timestamp": 8, "open": 9, "high": 9, "low": 9, "close": 9},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "backtest"
    assert payload["chain_id"] == 11155111
    assert payload["metrics"]["trades_count"] == 2
    assert payload["trades"][0]["action"] == "buy"
    assert payload["trades"][1]["action"] == "sell"


def test_run_backtest_rejects_invalid_strategy_windows() -> None:
    response = client.post(
        "/api/v1/backtests/run",
        json={
            "chain_id": 11155111,
            "asset": "WETH/USDC",
            "short_window": 3,
            "long_window": 3,
            "candles": [
                {"timestamp": 1, "open": 10, "high": 10, "low": 10, "close": 10},
                {"timestamp": 2, "open": 11, "high": 11, "low": 11, "close": 11},
                {"timestamp": 3, "open": 12, "high": 12, "low": 12, "close": 12},
                {"timestamp": 4, "open": 13, "high": 13, "low": 13, "close": 13},
            ],
        },
    )

    assert response.status_code == 422
