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
      --accent-3: #2563eb;
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
      max-width: 1280px;
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
    button.danger {
      background: var(--accent-2);
      border-color: var(--accent-2);
    }
    .layout {
      display: grid;
      grid-template-columns: minmax(0, 1.45fr) minmax(320px, 0.75fr);
      gap: 18px;
    }
    .stack { display: grid; gap: 18px; }
    .chart-wrap {
      height: 330px;
      margin-top: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfe;
      padding: 10px;
    }
    canvas {
      width: 100%;
      height: 100%;
      display: block;
    }
    .status-line {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-top: 12px;
      color: var(--muted);
      font-size: 13px;
    }
    .pill {
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 5px 9px;
      background: #ffffff;
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
    @media (max-width: 900px) {
      .layout { grid-template-columns: 1fr; }
      .chart-wrap { height: 260px; }
    }
  </style>
</head>
<body>
  <header>
    <h1>AlphaGuard AI Demo</h1>
    <p>
      Live market watch, strategy preview, paper-only trade intent,
      and no-execution backtesting.
    </p>
  </header>
  <main>
    <div class="layout">
      <div class="stack">
        <section>
          <h2>Market Watch</h2>
          <p>DexScreener live pair data with a local fixture price path for strategy preview.</p>
          <div class="grid">
            <label>Preset pair
              <select id="pairPreset"></select>
            </label>
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
          <div class="status-line">
            <span class="pill" id="selectedPair">WETH/USDC</span>
            <span class="pill">Mode: paper/backtest only</span>
            <span class="pill" id="lastUpdated">Not loaded</span>
          </div>
          <div class="chart-wrap">
            <canvas id="priceChart" width="900" height="330"></canvas>
          </div>
          <div class="metrics" id="pairMetrics"></div>
        </section>

        <section>
          <h2>Backtest</h2>
          <p>
            Runs the selected strategy against fixture candles until
            OHLCV provider wiring lands.
          </p>
          <div class="grid">
            <label>Strategy
              <select id="strategyName">
                <option value="moving_average_crossover">Moving average crossover</option>
              </select>
            </label>
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
      </div>

      <div class="stack">
        <section>
          <h2>Paper Trade Intent</h2>
          <p>
            Starts a local intent only. No wallet connection, signing,
            or transaction submission.
          </p>
          <div class="grid">
            <label>Side
              <select id="tradeSide">
                <option value="watch">Watch only</option>
                <option value="paper-buy">Paper buy</option>
                <option value="paper-sell">Paper sell</option>
              </select>
            </label>
            <label>Notional USD
              <input id="notionalUsd" type="number" value="100" min="1" />
            </label>
            <label>Action
              <button id="startPaperTrade" class="danger">Start Paper Trade</button>
            </label>
          </div>
          <div class="metrics" id="tradeIntent"></div>
        </section>

        <section>
          <h2>Raw Response</h2>
          <pre id="rawOutput">Ready.</pre>
        </section>
      </div>
    </div>
  </main>

  <script>
    const pairPresets = [
      {
        label: "Ethereum WETH/USDC",
        chainSlug: "ethereum",
        pairAddress: "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",
        asset: "WETH/USDC"
      },
      {
        label: "Ethereum WETH/USDT",
        chainSlug: "ethereum",
        pairAddress: "0x06da0fd433C1A5d7a4faa01111c044910A184553",
        asset: "WETH/USDT"
      },
      {
        label: "Base WETH/USDC",
        chainSlug: "base",
        pairAddress: "0x96d4b53A38337a5733179751781178a261330606",
        asset: "WETH/USDC"
      }
    ];

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
    let latestPair = null;

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

    function drawChart(candles, trades = []) {
      const canvas = document.getElementById("priceChart");
      const ctx = canvas.getContext("2d");
      const width = canvas.width;
      const height = canvas.height;
      const padding = 34;
      const closes = candles.map((candle) => candle.close);
      const min = Math.min(...closes);
      const max = Math.max(...closes);
      const range = Math.max(max - min, 1);

      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = "#fbfcfe";
      ctx.fillRect(0, 0, width, height);
      ctx.strokeStyle = "#d9dee7";
      ctx.lineWidth = 1;

      for (let index = 0; index < 5; index += 1) {
        const y = padding + ((height - padding * 2) / 4) * index;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
      }

      const pointFor = (candle, index) => {
        const x = padding + ((width - padding * 2) / (candles.length - 1)) * index;
        const y = height - padding - ((candle.close - min) / range) * (height - padding * 2);
        return { x, y };
      };

      ctx.strokeStyle = "#0f766e";
      ctx.lineWidth = 3;
      ctx.beginPath();
      candles.forEach((candle, index) => {
        const point = pointFor(candle, index);
        if (index === 0) ctx.moveTo(point.x, point.y);
        else ctx.lineTo(point.x, point.y);
      });
      ctx.stroke();

      ctx.fillStyle = "#17202a";
      ctx.font = "12px Arial";
      ctx.fillText(`High ${money(max)}`, padding, 18);
      ctx.fillText(`Low ${money(min)}`, padding, height - 12);

      trades.forEach((trade) => {
        const index = candles.findIndex((candle) => candle.timestamp === trade.timestamp);
        if (index < 0) return;
        const point = pointFor(candles[index], index);
        ctx.fillStyle = trade.action === "buy" ? "#2563eb" : "#b42318";
        ctx.beginPath();
        ctx.arc(point.x, point.y, 6, 0, Math.PI * 2);
        ctx.fill();
      });
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
        latestPair = payload;
        document.getElementById("selectedPair").textContent =
          `${payload.base_token.symbol}/${payload.quote_token.symbol}`;
        document.getElementById("lastUpdated").textContent = new Date().toLocaleTimeString();
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
        drawChart(fixtureCandles);
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
          asset: document.getElementById("selectedPair").textContent,
          strategy: document.getElementById("strategyName").value,
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
        drawChart(fixtureCandles, payload.trades);
        showRaw(payload);
      } catch (error) {
        metrics.innerHTML = `<span class="error">${JSON.stringify(error)}</span>`;
        showRaw(error);
      }
    }

    function startPaperTrade() {
      const side = document.getElementById("tradeSide").value;
      const notional = Number(document.getElementById("notionalUsd").value);
      const pair = latestPair
        ? `${latestPair.base_token.symbol}/${latestPair.quote_token.symbol}`
        : document.getElementById("selectedPair").textContent;
      const intent = {
        mode: "paper",
        side,
        pair,
        notional_usd: notional,
        status: side === "watch" ? "watching" : "intent_created",
        execution: "disabled"
      };
      document.getElementById("tradeIntent").innerHTML = [
        metric("Mode", "Paper only"),
        metric("Intent", intent.status),
        metric("Pair", pair),
        metric("Notional", `$${money(notional)}`)
      ].join("");
      showRaw(intent);
    }

    function initPairPresets() {
      const select = document.getElementById("pairPreset");
      select.innerHTML = pairPresets.map((preset, index) =>
        `<option value="${index}">${preset.label}</option>`
      ).join("");
      select.addEventListener("change", () => {
        const preset = pairPresets[Number(select.value)];
        document.getElementById("chainSlug").value = preset.chainSlug;
        document.getElementById("pairAddress").value = preset.pairAddress;
        document.getElementById("selectedPair").textContent = preset.asset;
      });
    }

    document.getElementById("loadPair").addEventListener("click", loadPair);
    document.getElementById("runBacktest").addEventListener("click", runBacktest);
    document.getElementById("startPaperTrade").addEventListener("click", startPaperTrade);
    initPairPresets();
    drawChart(fixtureCandles);
    loadPair();
    runBacktest();
  </script>
</body>
</html>
"""
