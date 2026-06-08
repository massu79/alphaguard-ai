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

Run the API:

```powershell
uvicorn app.main:app --reload
```

Open the docs at `http://127.0.0.1:8000/docs`.

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
