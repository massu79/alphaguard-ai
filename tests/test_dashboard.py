from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_renders_local_demo_page() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "AlphaGuard AI Demo" in response.text
    assert "/api/v1/market-data/pair" in response.text
    assert "/api/v1/backtests/run" in response.text
