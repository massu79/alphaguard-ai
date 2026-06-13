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
4. Run a no-execution strategy backtest with `POST /api/v1/backtests/run`.

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

## On-Chain Backtest MVP

The backtest API is designed around on-chain market data, but the current implementation only accepts normalized candle data supplied in the request. This keeps the MVP safe and testable while leaving room to swap the data provider for testnet RPC or an indexer later.

Safety boundaries:

- Default mode is `backtest`.
- No private keys are required.
- No transactions are built, signed, submitted, or simulated against a wallet.
- No blockchain RPC calls are made by the default inline data provider.

Example backtest request:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/backtests/run `
  -H "Content-Type: application/json" `
  -d "{\"chain_id\":11155111,\"asset\":\"WETH/USDC\",\"initial_cash\":120,\"short_window\":2,\"long_window\":3,\"candles\":[{\"timestamp\":1,\"open\":10,\"high\":10,\"low\":10,\"close\":10},{\"timestamp\":2,\"open\":9,\"high\":9,\"low\":9,\"close\":9},{\"timestamp\":3,\"open\":8,\"high\":8,\"low\":8,\"close\":8},{\"timestamp\":4,\"open\":12,\"high\":12,\"low\":12,\"close\":12},{\"timestamp\":5,\"open\":14,\"high\":14,\"low\":14,\"close\":14},{\"timestamp\":6,\"open\":13,\"high\":13,\"low\":13,\"close\":13},{\"timestamp\":7,\"open\":11,\"high\":11,\"low\":11,\"close\":11},{\"timestamp\":8,\"open\":9,\"high\":9,\"low\":9,\"close\":9}]}"
```

The endpoint returns trade events and summary metrics such as ending equity, total return, max drawdown, and trade count.

## Market Data Provider Foundation

The market data API provides the first swappable provider boundary for real on-chain data. The default `fixture` provider is local and deterministic; the `indexer` provider expects a normalized HTTP API at `ALPHAGUARD_MARKET_DATA_BASE_URL`.

Fetch fixture candles:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/market-data/candles `
  -H "Content-Type: application/json" `
  -d "{\"chain_id\":11155111,\"pool_address\":\"0xpool\",\"asset\":\"WETH/USDC\",\"interval\":\"1h\",\"limit\":8,\"provider\":\"fixture\"}"
```

Expected normalized indexer response shape:

```json
{
  "candles": [
    {
      "timestamp": 1717200000,
      "open": 100,
      "high": 110,
      "low": 95,
      "close": 105,
      "volume": 1234,
      "block_number": 12345678
    }
  ]
}
```

To swap in an indexer, set `ALPHAGUARD_MARKET_DATA_PROVIDER=indexer` and provide `ALPHAGUARD_MARKET_DATA_BASE_URL`. The indexer adapter reads data only; it does not build or submit transactions.

## Live Pair Data With DexScreener

The MVP can also read live pair metrics from DexScreener without an API key. This is read-only market data for display and analysis; it is not trading infrastructure.

Example request for the Ethereum Uniswap V2 WETH/USDC pair:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/market-data/pair `
  -H "Content-Type: application/json" `
  -d "{\"chain_slug\":\"ethereum\",\"pair_address\":\"0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc\"}"
```

The response includes token symbols, USD price, liquidity, volume, transaction counts, price changes, and pair metadata where available.

## Configuration

Copy `.env.example` to `.env` and adjust values as needed.

| Variable | Default | Description |
| --- | --- | --- |
| `ALPHAGUARD_APP_NAME` | `AlphaGuard AI` | API display name |
| `ALPHAGUARD_ENVIRONMENT` | `local` | Runtime environment label |
| `ALPHAGUARD_API_V1_PREFIX` | `/api/v1` | Versioned API route prefix |
| `ALPHAGUARD_CORS_ORIGINS` | `[]` | Comma-separated CORS origins |
| `ALPHAGUARD_TRADING_MODE` | `backtest` | Runtime trading mode; keep `backtest` for local MVP work |
| `ALPHAGUARD_TESTNET_RPC_URL` | `None` | Reserved for future testnet data provider work |
| `ALPHAGUARD_MARKET_DATA_PROVIDER` | `fixture` | Candle provider: `fixture` or `indexer` |
| `ALPHAGUARD_MARKET_DATA_BASE_URL` | `None` | Base URL for a normalized candle indexer |
| `ALPHAGUARD_MARKET_DATA_API_KEY` | `None` | Optional bearer token for the indexer provider |
| `ALPHAGUARD_PRODUCTION_TRADING_ENABLED` | `false` | Reserved kill switch; production trading is not implemented |

## Testing

```powershell
pytest
```
