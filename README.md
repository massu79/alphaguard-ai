# AlphaGuard AI

Human-approved AI agent for on-chain alpha detection and risk alerts.

This repository starts with a FastAPI MVP: a lightweight API surface for risk assessment workflows.

## Features

- FastAPI application factory with versioned API routing
- Health check endpoint for uptime probes
- MVP analysis endpoint with deterministic risk scoring
- Pydantic settings via environment variables
- Pytest coverage for core API behavior

## Project Structure

```text
app/
  api/v1/
    endpoints/
      analysis.py
      health.py
    router.py
  core/
    config.py
  models/
    analysis.py
  services/
    risk_analyzer.py
  main.py
tests/
  test_analysis.py
  test_health.py
```

## Getting Started

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -e ".[dev]"
```

Run the API locally:

```powershell
uvicorn app.main:app --reload
```

Open the docs at `http://127.0.0.1:8000/docs`.

For a quick smoke check:

```powershell
curl http://127.0.0.1:8000/health
```

## Current Demo Flow

The current MVP exposes a deterministic demo risk assessment flow. It does not call blockchain APIs, submit transactions, or execute trades.

1. Start the API with `uvicorn app.main:app --reload`.
2. Confirm the service is running with `GET /health` or `GET /api/v1/health`.
3. Submit weighted demo signals to `POST /api/v1/analysis/assess`.

Example request:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/analysis/assess `
  -H "Content-Type: application/json" `
  -d "{\"subject_id\":\"wallet-demo-1\",\"signals\":[{\"name\":\"failed_login_rate\",\"value\":0.8,\"weight\":2},{\"name\":\"profile_age_risk\",\"value\":0.2,\"weight\":1}]}"
```

Example response:

```json
{
  "subject_id": "wallet-demo-1",
  "score": 0.6,
  "level": "medium",
  "recommendation": "Review the subject and increase monitoring cadence."
}
```

## Configuration

Copy `.env.example` to `.env` and adjust values as needed.

| Variable | Default | Description |
| --- | --- | --- |
| `ALPHAGUARD_APP_NAME` | `AlphaGuard AI` | API display name |
| `ALPHAGUARD_ENVIRONMENT` | `local` | Runtime environment label |
| `ALPHAGUARD_API_V1_PREFIX` | `/api/v1` | Versioned API route prefix |
| `ALPHAGUARD_CORS_ORIGINS` | `[]` | Comma-separated CORS origins |

## Testing

```powershell
pytest
```
