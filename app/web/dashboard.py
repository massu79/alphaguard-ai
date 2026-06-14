from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard() -> str:
    return DASHBOARD_HTML


DASHBOARD_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AlphaGuard AI Demo</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f7f8fa;
      --panel: #ffffff;
      --ink: #17202a;
      --muted: #5f6b7a;
      --line: #d9dee7;
      --accent: #0f766e;
      --accent-2: #b42318;
      --code: #111827;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.45;
    }
    header {
      border-bottom: 1px solid var(--line);
      background: var(--panel);
      padding: 20px 24px;
    }
    main {
      display: grid;
      gap: 18px;
      max-width: 1180px;
      margin: 0 auto;
      padding: 20px;
    }
    h1, h2 { margin: 0; }
    h1 { font-size: 26px; }
    h2 { font-size: 18px; }
    p { margin: 6px 0 0; color: var(--muted); }
    section {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 10px;
      margin-top: 14px;
    }
    label {
      display: grid;
      gap: 5px;
      color: var(--muted);
      font-size: 13px;
    }
    input, select, button {
      min-height: 38px;
      border-radius: 6px;
      border: 1px solid var(--line);
      font: inherit;
      padding: 8px 10px;
    }
    button {
      cursor: pointer;
      color: #ffffff;
      background: var(--accent);
      border-color: var(--accent);
      font-weight: 700;
    }
    button.secondary {
      color: var(--ink);
      background: #eef2f7;
      border-color: var(--line);
    }
    .metrics {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 10px;
      margin-top: 14px;
    }
    .metric {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      min-height: 82px;
    }
    .metric span { display: block; color: var(--muted); font-size: 12px; }
    .metric strong { display: block; margin-top: 6px; font-size: 20px; }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      font-size: 14px;
    }
    th, td {
      border-bottom: 1px solid var(--line);
      padding: 9px 8px;
      text-align: left;
      vertical-align: top;
    }
    th { color: var(--muted); font-size: 12px; text-transform: uppercase; }
    pre {
      overflow: auto;
      background: var(--code);
      color: #f9fafb;
      border-radius: 8px;
      padding: 12px;
      min-height: 72px;
      white-space: pre-wrap;
    }
    .error { color: var(--accent-2); font-weight: 700; }
  </style>
</head>
<body>
  <header>
    <h1>AlphaGuard AI Demo</h1>
    <p>Read-only market data, fixture candles, and no-execution backtesting.</p>
  </header>
  <main>
    <section>
      <h2>Live Pair Data</h2>
      <p>Uses DexScreener public data. No wallet, private key, or transaction execution.</p>
      <div class="grid">
        <label>Chain slug
          <input id="chainSlug" value="ethereum" />
        </label>
        <label>Pair address
          <input id="pairAddress" value="0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc" />
        </label>
        <label>Action
          <button id="loadPair">Fetch Pair</button>
        </label>
      </div>
      <div class="metrics" id="pairMetrics"></div>
    </section>

    <section>
      <h2>Backtest Demo</h2>
      <p>Runs a moving-average crossover against fixture candle data.</p>
      <div class="grid">
        <label>Initial cash
          <input id="initialCash" type="number" value="120" min="1" />
        </label>
        <label>Short window
          <input id="shortWindow" type="number" value="2" min="1" />
        </label>
        <label>Long window
          <input id="longWindow" type="number" value="3" min="2" />
        </label>
        <label>Action
          <button id="runBacktest" class="secondary">Run Backtest</button>
        </label>
      </div>
      <div class="metrics" id="backtestMetrics"></div>
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>Action</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Cash After</th>
          </tr>
        </thead>
        <tbody id="tradeRows"></tbody>
      </table>
    </section>

    <section>
      <h2>Raw Response</h2>
      <pre id="rawOutput">Ready.</pre>
    </section>
  </main>

  <script>
    const fixtureCandles = [
      { timestamp: 1, open: 10, high: 10, low: 10, close: 10 },
      { timestamp: 2, open: 9, high: 9, low: 9, close: 9 },
      { timestamp: 3, open: 8, high: 8, low: 8, close: 8 },
      { timestamp: 4, open: 12, high: 12, low: 12, close: 12 },
      { timestamp: 5, open: 14, high: 14, low: 14, close: 14 },
      { timestamp: 6, open: 13, high: 13, low: 13, close: 13 },
      { timestamp: 7, open: 11, high: 11, low: 11, close: 11 },
      { timestamp: 8, open: 9, high: 9, low: 9, close: 9 }
    ];

    function money(value) {
      if (value === null || value === undefined) return "-";
      return Number(value).toLocaleString(undefined, { maximumFractionDigits: 4 });
    }

    function metric(label, value) {
      return `<div class="metric"><span>${label}</span><strong>${value}</strong></div>`;
    }

    function showRaw(value) {
      document.getElementById("rawOutput").textContent = JSON.stringify(value, null, 2);
    }

    async function postJson(path, body) {
      const response = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      const payload = await response.json();
      if (!response.ok) throw payload;
      return payload;
    }

    async function loadPair() {
      const metrics = document.getElementById("pairMetrics");
      metrics.innerHTML = "Loading...";
      try {
        const payload = await postJson("/api/v1/market-data/pair", {
          chain_slug: document.getElementById("chainSlug").value,
          pair_address: document.getElementById("pairAddress").value
        });
        metrics.innerHTML = [
          metric("Pair", `${payload.base_token.symbol}/${payload.quote_token.symbol}`),
          metric("Price USD", `$${money(payload.price_usd)}`),
          metric("Liquidity USD", `$${money(payload.liquidity && payload.liquidity.usd)}`),
          metric("24h Volume", `$${money(payload.volume.h24)}`),
          metric(
            "24h Txns",
            `${payload.txns.h24 ? payload.txns.h24.buys : 0} buys / ` +
            `${payload.txns.h24 ? payload.txns.h24.sells : 0} sells`
          ),
          metric("24h Change", `${money(payload.price_change.h24)}%`)
        ].join("");
        showRaw(payload);
      } catch (error) {
        metrics.innerHTML = `<span class="error">${JSON.stringify(error)}</span>`;
        showRaw(error);
      }
    }

    async function runBacktest() {
      const metrics = document.getElementById("backtestMetrics");
      const rows = document.getElementById("tradeRows");
      metrics.innerHTML = "Running...";
      rows.innerHTML = "";
      try {
        const payload = await postJson("/api/v1/backtests/run", {
          chain_id: 11155111,
          asset: "WETH/USDC",
          initial_cash: Number(document.getElementById("initialCash").value),
          short_window: Number(document.getElementById("shortWindow").value),
          long_window: Number(document.getElementById("longWindow").value),
          candles: fixtureCandles
        });
        metrics.innerHTML = [
          metric("Ending Equity", `$${money(payload.metrics.ending_equity)}`),
          metric("Return", `${money(payload.metrics.total_return_pct)}%`),
          metric("Max Drawdown", `${money(payload.metrics.max_drawdown_pct)}%`),
          metric("Trades", payload.metrics.trades_count)
        ].join("");
        rows.innerHTML = payload.trades.map((trade) => `
          <tr>
            <td>${trade.timestamp}</td>
            <td>${trade.action.toUpperCase()}</td>
            <td>${money(trade.price)}</td>
            <td>${money(trade.quantity)}</td>
            <td>${money(trade.cash_after)}</td>
          </tr>
        `).join("");
        showRaw(payload);
      } catch (error) {
        metrics.innerHTML = `<span class="error">${JSON.stringify(error)}</span>`;
        showRaw(error);
      }
    }

    document.getElementById("loadPair").addEventListener("click", loadPair);
    document.getElementById("runBacktest").addEventListener("click", runBacktest);
    loadPair();
    runBacktest();
  </script>
</body>
</html>
"""
