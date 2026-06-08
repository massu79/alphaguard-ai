from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_assess_risk_returns_weighted_score_and_level() -> None:
    response = client.post(
        "/api/v1/analysis/assess",
        json={
            "subject_id": "account-123",
            "signals": [
                {"name": "failed_login_rate", "value": 0.8, "weight": 2},
                {"name": "profile_age_risk", "value": 0.2, "weight": 1},
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "subject_id": "account-123",
        "score": 0.6,
        "level": "medium",
        "recommendation": "Review the subject and increase monitoring cadence.",
    }


def test_assess_risk_requires_at_least_one_signal() -> None:
    response = client.post(
        "/api/v1/analysis/assess",
        json={"subject_id": "account-123", "signals": []},
    )

    assert response.status_code == 422
