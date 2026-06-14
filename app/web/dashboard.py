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
    .hero-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
    }
    .hero-card {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      padding: 14px;
      min-height: 96px;
    }
    .hero-card span {
      display: block;
      color: var(--muted);
      font-size: 12px;
    }
    .hero-card strong {
      display: block;
      margin-top: 8px;
      font-size: 22px;
    }
    .signal-bar {
      height: 8px;
      border-radius: 999px;
      background: #e5e7eb;
      overflow: hidden;
      margin-top: 10px;
    }
    .signal-bar div {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #b42318, #f59e0b, #0f766e);
      transition: width 180ms ease;
    }
    .chart-wrap {
      height: 390px;
      margin-top: 14px;
      border: 1px solid #263241;
      border-radius: 8px;
      background: #0b1118;
      padding: 0;
      position: relative;
      overflow: hidden;
    }
    .real-chart-wrap {
      height: 430px;
      margin-top: 14px;
      border: 1px solid #263241;
      border-radius: 8px;
      background: #0b1118;
      overflow: hidden;
    }
    .real-chart-wrap iframe {
      width: 100%;
      height: 100%;
      border: 0;
      display: block;
    }
    .chart-toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      min-height: 38px;
      padding: 8px 10px;
      border-bottom: 1px solid #263241;
      color: #cbd5e1;
      font-size: 12px;
    }
    .chart-toolbar strong {
      color: #f8fafc;
      font-size: 13px;
    }
    .chart-badge {
      border: 1px solid #334155;
      border-radius: 999px;
      padding: 4px 8px;
      background: #111827;
    }
    canvas {
      width: 100%;
      height: calc(100% - 38px);
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
    .position-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 8px;
      margin-top: 12px;
    }
    .position-tile {
      border: 1px solid #263241;
      border-radius: 8px;
      background: #0f172a;
      color: #e5e7eb;
      padding: 10px;
      min-height: 66px;
    }
    .position-tile span {
      display: block;
      color: #94a3b8;
      font-size: 11px;
    }
    .position-tile strong {
      display: block;
      margin-top: 5px;
      font-size: 17px;
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
      .chart-wrap { height: 320px; }
      .real-chart-wrap { height: 360px; }
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
    <section>
      <h2>Mantle AI Trading Cockpit</h2>
      <p>
        Mantle Sepolia connectivity, live market reference, paper execution,
        risk controls, and auditable strategy decisions.
      </p>
      <div class="hero-grid">
        <div class="hero-card">
          <span>Network</span>
          <strong id="heroNetwork">Mantle Sepolia</strong>
        </div>
        <div class="hero-card">
          <span>Latest Block</span>
          <strong id="heroBlock">Checking...</strong>
        </div>
        <div class="hero-card">
          <span>Alpha Signal</span>
          <strong id="heroSignal">Pending</strong>
          <div class="signal-bar"><div id="heroSignalBar"></div></div>
        </div>
        <div class="hero-card">
          <span>Risk Mode</span>
          <strong>Paper only</strong>
        </div>
      </div>
    </section>

    <div class="layout">
      <div class="stack">
        <section>
          <h2>Market Watch</h2>
          <p>DexScreener live pair data with a local fixture price path for strategy preview.</p>
          <div class="grid">
            <label>Preset pair
              <select id="pairPreset"></select>
            </label>
            <label>Real chart
              <select id="realChartPreset">
                <option value="BYBIT:MNTUSDT">TradingView MNTUSDT</option>
                <option value="BINANCE:ETHUSDT">TradingView ETHUSDT</option>
                <option value="COINBASE:ETHUSD">TradingView ETHUSD</option>
              </select>
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
          <div class="real-chart-wrap">
            <iframe
              id="realChartFrame"
              title="TradingView real market chart"
              loading="lazy"
              src="https://www.tradingview.com/widgetembed/?symbol=BYBIT%3AMNTUSDT&interval=60&theme=dark&style=1&timezone=Etc%2FUTC&withdateranges=1&hideideas=1&saveimage=0"
            ></iframe>
          </div>
          <div class="chart-wrap">
            <div class="chart-toolbar">
              <strong id="chartTitle">MNT/USDT - Local Position Map</strong>
              <span class="chart-badge">Paper TP/SL overlay</span>
            </div>
            <canvas id="priceChart" width="900" height="330"></canvas>
          </div>
          <div class="position-strip" id="activePositionStrip"></div>
          <div class="metrics" id="pairMetrics"></div>
        </section>

        <section>
          <h2>Alpha Signal</h2>
          <p>
            Transparent scoring from momentum, liquidity, volume, risk, and
            Mantle network freshness.
          </p>
          <div class="metrics" id="alphaMetrics"></div>
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
          <h2>Mantle Sepolia</h2>
          <p>
            Read-only testnet connection for hackathon demos.
            Chain ID 5003, no signing or transaction submission.
          </p>
          <div class="grid">
            <label>Wallet address
              <input
                id="mantleAddress"
                value="0x0000000000000000000000000000000000000000"
              />
            </label>
            <label>Network
              <button id="checkMantle">Check RPC</button>
            </label>
            <label>Balance
              <button id="checkMantleBalance" class="secondary">Check MNT</button>
            </label>
          </div>
          <div class="metrics" id="mantleMetrics"></div>
        </section>

        <section>
          <h2>Paper Trading</h2>
          <p>
            Creates local paper positions only. No wallet connection,
            signing, or transaction submission.
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
            <label>Take profit %
              <input id="takeProfitPct" type="number" value="6" min="0.1" step="0.1" />
            </label>
            <label>Stop loss %
              <input id="stopLossPct" type="number" value="3" min="0.1" step="0.1" />
            </label>
            <label>Action
              <button id="startPaperTrade" class="danger">Start Paper Trade</button>
            </label>
          </div>
          <div class="metrics" id="tradeIntent"></div>
          <table>
            <thead>
              <tr>
                <th>Side</th>
                <th>Pair</th>
                <th>Entry</th>
                <th>Mark</th>
                <th>PnL</th>
              </tr>
            </thead>
            <tbody id="paperRows"></tbody>
          </table>
        </section>

        <section>
          <h2>Raw Response</h2>
          <pre id="rawOutput">Ready.</pre>
        </section>

        <section>
          <h2>Strategy Audit Log</h2>
          <p>Every paper decision is written here for reproducibility.</p>
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>Event</th>
                <th>Signal</th>
                <th>Decision</th>
              </tr>
            </thead>
            <tbody id="auditRows"></tbody>
          </table>
        </section>
      </div>
    </div>
  </main>

  <script>
    const pairPresets = [
      {
        label: "Mantle MNT/USDT Demo",
        chainSlug: "mantle",
        pairAddress: "demo-mnt-usdt",
        asset: "MNT/USDT",
        demo: true
      },
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
      { timestamp: 1, open: 10.2, high: 10.8, low: 9.7, close: 10.0, volume: 1100 },
      { timestamp: 2, open: 10.0, high: 10.2, low: 8.8, close: 9.0, volume: 1600 },
      { timestamp: 3, open: 9.0, high: 9.4, low: 7.8, close: 8.0, volume: 2100 },
      { timestamp: 4, open: 8.0, high: 12.4, low: 7.9, close: 12.0, volume: 3200 },
      { timestamp: 5, open: 12.0, high: 14.6, low: 11.7, close: 14.0, volume: 2800 },
      { timestamp: 6, open: 14.0, high: 14.3, low: 12.6, close: 13.0, volume: 1800 },
      { timestamp: 7, open: 13.0, high: 13.2, low: 10.5, close: 11.0, volume: 2300 },
      { timestamp: 8, open: 11.0, high: 11.4, low: 8.7, close: 9.0, volume: 2600 }
    ];
    let latestPair = null;
    let paperPositions = [];
    let activeCandles = fixtureCandles.map((candle) => ({ ...candle }));
    let liveTick = 0;
    let mantleStatus = null;
    let auditLog = [];

    function tradingViewUrl(symbol) {
      return "https://www.tradingview.com/widgetembed/?" + new URLSearchParams({
        symbol,
        interval: "60",
        theme: "dark",
        style: "1",
        timezone: "Etc/UTC",
        withdateranges: "1",
        hideideas: "1",
        saveimage: "0"
      }).toString();
    }

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

    function latestPrice() {
      if (activeCandles.length) return activeCandles[activeCandles.length - 1].close;
      if (latestPair && latestPair.price_usd) return Number(latestPair.price_usd);
      return fixtureCandles[fixtureCandles.length - 1].close;
    }

    function alphaSignal() {
      const last = activeCandles[activeCandles.length - 1];
      const previous = activeCandles[activeCandles.length - 5] || activeCandles[0];
      const momentumPct = ((last.close - previous.close) / previous.close) * 100;
      const volumeAvg = activeCandles.reduce((sum, candle) => sum + (candle.volume || 0), 0) /
        activeCandles.length;
      const volumeSpike = ((last.volume || 0) / Math.max(volumeAvg, 1)) * 100;
      const liquidityScore = latestPair && latestPair.liquidity && latestPair.liquidity.usd
        ? Math.min(latestPair.liquidity.usd / 1000000, 1) * 100
        : 62;
      const riskPenalty = paperPositions.length > 2 ? 18 : paperPositions.length * 6;
      const freshness = mantleStatus ? 92 : 70;
      const rawScore = momentumPct * 4
        + volumeSpike * 0.2
        + liquidityScore * 0.25
        + freshness * 0.2
        - riskPenalty;
      const score = Math.max(
        Math.min(rawScore, 100),
        0
      );
      let decision = "WATCH";
      if (score >= 70) decision = "LONG BIAS";
      else if (score <= 35) decision = "RISK OFF";
      return {
        score,
        decision,
        momentumPct,
        volumeSpike,
        liquidityScore,
        freshness,
        riskPenalty
      };
    }

    function renderAlphaSignal() {
      const signal = alphaSignal();
      document.getElementById("heroSignal").textContent =
        `${signal.decision} ${money(signal.score)}`;
      document.getElementById("heroSignalBar").style.width = `${signal.score}%`;
      document.getElementById("alphaMetrics").innerHTML = [
        metric("Decision", signal.decision),
        metric("Score", money(signal.score)),
        metric("Momentum", `${money(signal.momentumPct)}%`),
        metric("Volume Spike", `${money(signal.volumeSpike)}%`),
        metric("Liquidity", money(signal.liquidityScore)),
        metric("Risk Penalty", `-${money(signal.riskPenalty)}`)
      ].join("");
      return signal;
    }

    function addAudit(event, decision, signal = alphaSignal()) {
      auditLog = [{
        time: new Date().toLocaleTimeString(),
        event,
        signal: `${signal.decision} ${money(signal.score)}`,
        decision
      }].concat(auditLog).slice(0, 8);
      renderAuditLog();
    }

    function renderAuditLog() {
      const rows = document.getElementById("auditRows");
      rows.innerHTML = auditLog.map((item) => `
        <tr>
          <td>${item.time}</td>
          <td>${item.event}</td>
          <td>${item.signal}</td>
          <td>${item.decision}</td>
        </tr>
      `).join("");
      if (!auditLog.length) {
        rows.innerHTML = `
          <tr>
            <td colspan="4">No strategy decisions yet.</td>
          </tr>
        `;
      }
    }

    function drawChart(candles, trades = [], positions = paperPositions) {
      const canvas = document.getElementById("priceChart");
      const ctx = canvas.getContext("2d");
      const width = canvas.width;
      const height = canvas.height;
      const pricePadLeft = 42;
      const pricePadRight = 76;
      const pricePadTop = 22;
      const pricePadBottom = 86;
      const volumeHeight = 54;
      const plotWidth = width - pricePadLeft - pricePadRight;
      const plotHeight = height - pricePadTop - pricePadBottom;
      const positionPrices = positions.flatMap((position) => [
        position.entry_price,
        position.take_profit,
        position.stop_loss
      ]);
      const highs = candles.map((candle) => candle.high).concat(positionPrices);
      const lows = candles.map((candle) => candle.low).concat(positionPrices);
      const volumes = candles.map((candle) => candle.volume || 0);
      const rawMin = Math.min(...lows);
      const rawMax = Math.max(...highs);
      const rawRange = Math.max(rawMax - rawMin, rawMax * 0.018, 0.01);
      const min = rawMin - rawRange * 0.55;
      const max = rawMax + rawRange * 0.55;
      const maxVolume = Math.max(...volumes, 1);
      const range = Math.max(max - min, 1);
      const candleSlot = plotWidth / candles.length;
      const bodyWidth = Math.max(Math.min(candleSlot * 0.58, 18), 6);

      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = "#0b1118";
      ctx.fillRect(0, 0, width, height);
      ctx.strokeStyle = "#1f2937";
      ctx.lineWidth = 1;

      for (let index = 0; index < 5; index += 1) {
        const y = pricePadTop + (plotHeight / 4) * index;
        ctx.beginPath();
        ctx.moveTo(pricePadLeft, y);
        ctx.lineTo(width - pricePadRight + 12, y);
        ctx.stroke();
        const price = max - (range / 4) * index;
        ctx.fillStyle = "#94a3b8";
        ctx.font = "11px Arial";
        ctx.fillText(money(price), width - pricePadRight + 20, y + 4);
      }

      const pointFor = (candle, index) => {
        const x = pricePadLeft + candleSlot * index + candleSlot / 2;
        const y = pricePadTop + ((max - candle.close) / range) * plotHeight;
        return { x, y };
      };
      const yForPrice = (price) => pricePadTop + ((max - price) / range) * plotHeight;

      const drawPriceLine = (price, label, color) => {
        const y = yForPrice(price);
        if (y < pricePadTop - 8 || y > pricePadTop + plotHeight + 8) return;
        ctx.strokeStyle = color;
        ctx.setLineDash([6, 4]);
        ctx.beginPath();
        ctx.moveTo(pricePadLeft, y);
        ctx.lineTo(width - pricePadRight + 12, y);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = color;
        ctx.fillRect(width - pricePadRight + 15, y - 10, 58, 20);
        ctx.fillStyle = "#0b1118";
        ctx.font = "11px Arial";
        ctx.fillText(label, width - pricePadRight + 20, y + 4);
      };

      candles.forEach((candle, index) => {
        const point = pointFor(candle, index);
        const openY = yForPrice(candle.open);
        const closeY = yForPrice(candle.close);
        const highY = yForPrice(candle.high);
        const lowY = yForPrice(candle.low);
        const isUp = candle.close >= candle.open;
        const color = isUp ? "#22ab94" : "#f23645";
        const volumeTop = height - 24 - ((candle.volume || 0) / maxVolume) * volumeHeight;

        ctx.strokeStyle = color;
        ctx.fillStyle = color;
        ctx.globalAlpha = 0.35;
        ctx.fillRect(
          point.x - bodyWidth / 2,
          volumeTop,
          bodyWidth,
          height - 24 - volumeTop
        );
        ctx.globalAlpha = 1;

        ctx.beginPath();
        ctx.moveTo(point.x, highY);
        ctx.lineTo(point.x, lowY);
        ctx.stroke();

        ctx.fillRect(
          point.x - bodyWidth / 2,
          Math.min(openY, closeY),
          bodyWidth,
          Math.max(Math.abs(closeY - openY), 2)
        );

        if (index % 2 === 0 || index === candles.length - 1) {
          ctx.fillStyle = "#64748b";
          ctx.font = "11px Arial";
          ctx.fillText(String(candle.timestamp), point.x - 4, height - 8);
        }
      });

      const last = candles[candles.length - 1];
      const lastY = yForPrice(last.close);
      positions.forEach((position) => {
        drawPriceLine(position.take_profit, "TP", "#22ab94");
        drawPriceLine(position.entry_price, "ENTRY", "#3b82f6");
        drawPriceLine(position.stop_loss, "SL", "#f23645");
      });
      drawPriceLine(last.close, money(last.close), "#f59e0b");

      ctx.fillStyle = "#cbd5e1";
      ctx.font = "12px Arial";
      ctx.fillText("MNT/USDT 1H - live forming candle", pricePadLeft, 17);

      trades.forEach((trade) => {
        const index = candles.findIndex((candle) => candle.timestamp === trade.timestamp);
        if (index < 0) return;
        const point = pointFor(candles[index], index);
        ctx.fillStyle = trade.action === "buy" ? "#3b82f6" : "#ef4444";
        ctx.beginPath();
        ctx.arc(point.x, point.y - 16, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#e5e7eb";
        ctx.font = "10px Arial";
        ctx.fillText(trade.action.toUpperCase(), point.x - 10, point.y - 24);
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

    async function getJson(path) {
      const response = await fetch(path);
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
        document.getElementById("chartTitle").textContent =
          `${payload.base_token.symbol}/${payload.quote_token.symbol} - 1H`;
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
        renderPaperPositions();
        renderAlphaSignal();
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
          candles: activeCandles
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
        addAudit("Backtest", `${payload.metrics.trades_count} trades generated`);
        drawChart(activeCandles, payload.trades);
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
      const entryPrice = latestPrice();
      const takeProfitPct = Number(document.getElementById("takeProfitPct").value) / 100;
      const stopLossPct = Number(document.getElementById("stopLossPct").value) / 100;
      if (side !== "watch") {
        const isLong = side === "paper-buy";
        paperPositions.push({
          side,
          pair,
          notional_usd: notional,
          entry_price: entryPrice,
          take_profit: isLong ? entryPrice * (1 + takeProfitPct) : entryPrice * (1 - takeProfitPct),
          stop_loss: isLong ? entryPrice * (1 - stopLossPct) : entryPrice * (1 + stopLossPct),
          quantity: entryPrice ? notional / entryPrice : 0,
          opened_at: new Date().toISOString()
        });
      }
      const intent = {
        mode: "paper",
        side,
        pair,
        notional_usd: notional,
        entry_price: entryPrice,
        take_profit_pct: takeProfitPct * 100,
        stop_loss_pct: stopLossPct * 100,
        status: side === "watch" ? "watching" : "intent_created",
        execution: "disabled"
      };
      renderPaperPositions();
      const signal = renderAlphaSignal();
      addAudit(
        "Paper trade",
        `${side.replace("paper-", "").toUpperCase()} ${pair} @ ${money(entryPrice)}`,
        signal
      );
      drawChart(activeCandles);
      document.getElementById("tradeIntent").innerHTML = [
        metric("Mode", "Paper only"),
        metric("Intent", intent.status),
        metric("Pair", pair),
        metric("Notional", `$${money(notional)}`),
        metric("Entry", `$${money(entryPrice)}`)
      ].join("");
      showRaw(intent);
    }

    function paperPnl(position, markPrice) {
      if (!markPrice) return 0;
      const direction = position.side === "paper-buy" ? 1 : -1;
      return (markPrice - position.entry_price) * position.quantity * direction;
    }

    function renderPaperPositions() {
      const rows = document.getElementById("paperRows");
      const strip = document.getElementById("activePositionStrip");
      const markPrice = latestPrice();
      const totalPnl = paperPositions.reduce(
        (sum, position) => sum + paperPnl(position, markPrice),
        0
      );
      const active = paperPositions[paperPositions.length - 1];
      strip.innerHTML = [
        positionTile("Position", active ? active.pair : "No active position"),
        positionTile("Mark", `$${money(markPrice)}`),
        positionTile("Unrealized PnL", `$${money(totalPnl)}`, totalPnl >= 0),
        positionTile(
          "TP / SL",
          active ? `${money(active.take_profit)} / ${money(active.stop_loss)}` : "-"
        )
      ].join("");
      rows.innerHTML = paperPositions.map((position) => {
        const pnl = paperPnl(position, markPrice);
        const color = pnl >= 0 ? "#0f766e" : "#b42318";
        return `
          <tr>
            <td>${position.side.replace("paper-", "").toUpperCase()}</td>
            <td>${position.pair}</td>
            <td>${money(position.entry_price)}</td>
            <td>${money(markPrice)}</td>
            <td style="color:${color};font-weight:700;">${money(pnl)}</td>
          </tr>
        `;
      }).join("");
      if (!paperPositions.length) {
        rows.innerHTML = `
          <tr>
            <td colspan="5">No paper positions yet.</td>
          </tr>
        `;
      }
    }

    function positionTile(label, value, positive = null) {
      const color = positive === null ? "#e5e7eb" : positive ? "#22ab94" : "#f23645";
      return `
        <div class="position-tile">
          <span>${label}</span>
          <strong style="color:${color};">${value}</strong>
        </div>
      `;
    }

    function buildMntDemoCandles() {
      return [
        0.628, 0.642, 0.633, 0.651, 0.668, 0.659, 0.681, 0.703,
        0.687, 0.711, 0.736, 0.718, 0.752, 0.779, 0.744, 0.768
      ].map((close, index, values) => {
        const open = index === 0 ? close * 0.995 : values[index - 1];
        const drift = Math.sin(index + 1) * 0.012;
        return {
          timestamp: index + 1,
          open,
          high: Math.max(open, close) + Math.abs(drift) + 0.004,
          low: Math.min(open, close) - Math.abs(drift) - 0.003,
          close,
          volume: 1200 + index * 115
        };
      });
    }

    function tickChart() {
      const last = activeCandles[activeCandles.length - 1];
      const direction = Math.sin(liveTick / 2) * 0.006 + (Math.random() - 0.5) * 0.004;
      const close = Math.max(last.close * (1 + direction), 0.0001);
      const forming = {
        ...last,
        high: Math.max(last.high, close),
        low: Math.min(last.low, close),
        close,
        volume: Math.max((last.volume || 1000) + 35 + Math.random() * 70, 1)
      };
      activeCandles = activeCandles.slice(0, -1).concat(forming);
      liveTick += 1;
      renderPaperPositions();
      renderAlphaSignal();
      drawChart(activeCandles);
    }

    async function checkMantle() {
      const metrics = document.getElementById("mantleMetrics");
      metrics.innerHTML = "Checking...";
      try {
        const payload = await getJson("/api/v1/chains/mantle-sepolia/status");
        mantleStatus = payload;
        document.getElementById("heroNetwork").textContent = payload.name;
        document.getElementById("heroBlock").textContent = payload.latest_block;
        metrics.innerHTML = [
          metric("Network", payload.name),
          metric("Chain ID", payload.chain_id),
          metric("Latest Block", payload.latest_block),
          metric("Currency", payload.currency_symbol)
        ].join("");
        renderAlphaSignal();
        addAudit("Mantle RPC", `Block ${payload.latest_block} verified`);
        showRaw(payload);
      } catch (error) {
        metrics.innerHTML = `<span class="error">${JSON.stringify(error)}</span>`;
        showRaw(error);
      }
    }

    async function checkMantleBalance() {
      const metrics = document.getElementById("mantleMetrics");
      metrics.innerHTML = "Checking balance...";
      try {
        const payload = await postJson("/api/v1/chains/mantle-sepolia/balance", {
          address: document.getElementById("mantleAddress").value
        });
        metrics.innerHTML = [
          metric("Address", `${payload.address.slice(0, 6)}...${payload.address.slice(-4)}`),
          metric("Balance", `${money(payload.balance_native)} ${payload.currency_symbol}`),
          metric("Wei", payload.balance_wei),
          metric("Chain ID", payload.chain_id)
        ].join("");
        showRaw(payload);
      } catch (error) {
        metrics.innerHTML = `<span class="error">${JSON.stringify(error)}</span>`;
        showRaw(error);
      }
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
        if (preset.demo) {
          activeCandles = buildMntDemoCandles();
          latestPair = {
            base_token: { symbol: "MNT" },
            quote_token: { symbol: "USDT" },
            price_usd: activeCandles[activeCandles.length - 1].close
          };
          document.getElementById("chartTitle").textContent =
            `${preset.asset} - Local Position Map`;
          renderPaperPositions();
          drawChart(activeCandles);
        }
      });
    }

    document.getElementById("loadPair").addEventListener("click", loadPair);
    document.getElementById("runBacktest").addEventListener("click", runBacktest);
    document.getElementById("startPaperTrade").addEventListener("click", startPaperTrade);
    document.getElementById("checkMantle").addEventListener("click", checkMantle);
    document.getElementById("checkMantleBalance").addEventListener("click", checkMantleBalance);
    document.getElementById("realChartPreset").addEventListener("change", (event) => {
      document.getElementById("realChartFrame").src = tradingViewUrl(event.target.value);
    });
    initPairPresets();
    activeCandles = buildMntDemoCandles();
    document.getElementById("pairPreset").value = "0";
    document.getElementById("chainSlug").value = pairPresets[0].chainSlug;
    document.getElementById("pairAddress").value = pairPresets[0].pairAddress;
    document.getElementById("selectedPair").textContent = pairPresets[0].asset;
    drawChart(activeCandles);
    renderPaperPositions();
    renderAlphaSignal();
    renderAuditLog();
    runBacktest();
    checkMantle();
    setInterval(tickChart, 2500);
  </script>
</body>
</html>
"""
