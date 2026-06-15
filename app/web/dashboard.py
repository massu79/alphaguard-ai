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
    .product-head {
      max-width: 1280px;
      margin: 0 auto;
      display: grid;
      gap: 12px;
    }
    .product-head h1 {
      font-size: 30px;
      max-width: 820px;
    }
    .product-head p {
      max-width: 760px;
      font-size: 15px;
    }
    .capability-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 8px;
      margin-top: 4px;
    }
    .capability {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f8fafc;
      padding: 10px 12px;
      min-height: 68px;
    }
    .capability span {
      color: var(--muted);
      display: block;
      font-size: 11px;
      text-transform: uppercase;
    }
    .capability strong {
      display: block;
      margin-top: 4px;
      font-size: 15px;
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
      margin-top: 14px;
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
    .strategy-hero {
      display: grid;
      grid-template-columns: minmax(260px, 0.75fr) minmax(0, 1.25fr);
      gap: 14px;
      margin-top: 14px;
    }
    .recommendation {
      border: 1px solid #263241;
      border-radius: 8px;
      background: #0f172a;
      color: #e5e7eb;
      padding: 16px;
    }
    .recommendation span {
      color: #94a3b8;
      display: block;
      font-size: 12px;
    }
    .recommendation strong {
      display: block;
      font-size: 34px;
      margin: 8px 0 6px;
    }
    .reason-list {
      margin: 12px 0 0;
      padding-left: 18px;
      color: #cbd5e1;
    }
    .reason-list li { margin: 5px 0; }
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
      .strategy-hero { grid-template-columns: 1fr; }
      .real-chart-wrap { height: 360px; }
    }
  </style>
</head>
<body>
  <header>
    <div class="product-head">
      <h1>MNT/USDT Paper-Trading Strategy Cockpit</h1>
      <p>
        Select an AI strategy, open a simulated position, watch live PnL with
        TP/SL, and validate the same idea with a fixture backtest.
      </p>
      <div class="capability-strip">
        <div class="capability">
          <span>1. Strategy</span>
          <strong>Choose Momentum, Reversion, or Liquidity</strong>
        </div>
        <div class="capability">
          <span>2. Trade</span>
          <strong>Start paper-only MNT/USDT exposure</strong>
        </div>
        <div class="capability">
          <span>3. Monitor</span>
          <strong>Track PnL, entry, TP, and SL live</strong>
        </div>
        <div class="capability">
          <span>4. Validate</span>
          <strong>Run a no-execution backtest</strong>
        </div>
      </div>
    </div>
  </header>
  <main>
    <section>
      <h2>Trade Setup</h2>
      <p>
        MNT/USDT is the demo pair. The app opens local paper positions only;
        no wallet signing or real execution is enabled.
      </p>
      <div class="strategy-hero">
        <div>
          <div class="grid">
            <label>Strategy
              <select id="primaryStrategy">
                <option value="momentum_breakout">Momentum Breakout</option>
                <option value="mean_reversion">Mean Reversion</option>
                <option value="liquidity_surge">Liquidity Surge</option>
              </select>
            </label>
            <label>Position size
              <input id="heroNotionalUsd" type="number" value="1000" min="1" />
            </label>
            <label>Action
              <button id="heroStartTrade">Start MNT/USDT Paper Trade</button>
            </label>
          </div>
          <div class="status-line">
            <span class="pill" id="dataFreshness">Data: Mantle Sepolia live</span>
            <span class="pill">Execution: paper only</span>
          </div>
        </div>
        <div class="recommendation">
          <span>Current recommendation</span>
          <strong id="heroSignal">Pending</strong>
          <div class="signal-bar"><div id="heroSignalBar"></div></div>
          <ul class="reason-list" id="recommendationReasons">
            <li>Waiting for market data.</li>
          </ul>
        </div>
      </div>
      <div class="hero-grid">
        <div class="hero-card">
          <span>Active Position</span>
          <strong id="heroPosition">No position</strong>
        </div>
        <div class="hero-card">
          <span>Simulated PnL</span>
          <strong id="heroPnl">$0</strong>
        </div>
        <div class="hero-card">
          <span>TP / SL</span>
          <strong id="heroTpSl">-</strong>
        </div>
        <div class="hero-card">
          <span>Data Freshness</span>
          <strong id="heroBlock">Checking...</strong>
        </div>
      </div>
    </section>

    <div class="layout">
      <div class="stack">
        <section>
          <h2>Market Watch</h2>
          <p>
            TradingView is the visual market reference. Paper positions use a
            simulated mark price until live OHLCV wiring is added.
          </p>
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
                <th>Sim Mark</th>
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
    const strategyProfiles = {
      momentum_breakout: {
        label: "Momentum Breakout",
        good: "Long only when trend and volume expand together.",
        watch: "Wait for breakout confirmation before adding risk.",
        risk: "Stand down when momentum fades or position risk is already high."
      },
      mean_reversion: {
        label: "Mean Reversion",
        good: "Look for a controlled long after a sharp pullback.",
        watch: "Wait for price to stretch away from the recent range.",
        risk: "Avoid fading the move while volatility is expanding."
      },
      liquidity_surge: {
        label: "Liquidity Surge",
        good: "Follow pairs where depth and activity support execution.",
        watch: "Liquidity is acceptable, but confirmation is not strong yet.",
        risk: "Do not add exposure when liquidity or freshness is weak."
      }
    };

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
      const strategy = document.getElementById("primaryStrategy").value;
      const momentumPct = ((last.close - previous.close) / previous.close) * 100;
      const volumeAvg = activeCandles.reduce((sum, candle) => sum + (candle.volume || 0), 0) /
        activeCandles.length;
      const volumeSpike = ((last.volume || 0) / Math.max(volumeAvg, 1)) * 100;
      const liquidityScore = latestPair && latestPair.liquidity && latestPair.liquidity.usd
        ? Math.min(latestPair.liquidity.usd / 1000000, 1) * 100
        : 62;
      const riskPenalty = paperPositions.length > 2 ? 18 : paperPositions.length * 6;
      const freshness = mantleStatus ? 92 : 70;
      const strategyWeights = {
        momentum_breakout: { momentum: 4, volume: 0.2, liquidity: 0.25, freshness: 0.2 },
        mean_reversion: { momentum: -2.5, volume: 0.12, liquidity: 0.35, freshness: 0.25 },
        liquidity_surge: { momentum: 2, volume: 0.25, liquidity: 0.45, freshness: 0.25 }
      }[strategy];
      const rawScore = momentumPct * strategyWeights.momentum
        + volumeSpike * strategyWeights.volume
        + liquidityScore * strategyWeights.liquidity
        + freshness * strategyWeights.freshness
        - riskPenalty;
      const score = Math.max(
        Math.min(rawScore, 100),
        0
      );
      let decision = "WATCH";
      if (score >= 70) decision = "LONG BIAS";
      else if (score <= 35) decision = "RISK OFF";
      const profile = strategyProfiles[strategy];
      const reasons = [
        profile[decision === "LONG BIAS" ? "good" : decision === "RISK OFF" ? "risk" : "watch"],
        `Momentum is ${money(momentumPct)}% over the recent candle window.`,
        `Volume is ${money(volumeSpike)}% of its local average.`,
        `Open paper positions add a ${money(riskPenalty)} point risk adjustment.`
      ];
      return {
        score,
        decision,
        strategy,
        strategyLabel: profile.label,
        momentumPct,
        volumeSpike,
        liquidityScore,
        freshness,
        riskPenalty,
        reasons
      };
    }

    function renderAlphaSignal() {
      const signal = alphaSignal();
      document.getElementById("heroSignal").textContent =
        `${signal.decision} ${money(signal.score)}`;
      document.getElementById("heroSignalBar").style.width = `${signal.score}%`;
      document.getElementById("recommendationReasons").innerHTML =
        signal.reasons.map((reason) => `<li>${reason}</li>`).join("");
      document.getElementById("alphaMetrics").innerHTML = [
        metric("Strategy", signal.strategyLabel),
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
      document.getElementById("heroPosition").textContent = active
        ? `${active.side.replace("paper-", "").toUpperCase()} ${active.pair}`
        : "No position";
      document.getElementById("heroPnl").textContent = `$${money(totalPnl)}`;
      document.getElementById("heroPnl").style.color = totalPnl >= 0 ? "#0f766e" : "#b42318";
      document.getElementById("heroTpSl").textContent = active
        ? `$${money(active.take_profit)} / $${money(active.stop_loss)}`
        : "-";
      strip.innerHTML = [
        positionTile("Position", active ? active.pair : "No active position"),
        positionTile("Sim Mark", `$${money(markPrice)}`),
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

    function tickPaperMark() {
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
    }

    async function checkMantle() {
      const metrics = document.getElementById("mantleMetrics");
      metrics.innerHTML = "Checking...";
      try {
        const payload = await getJson("/api/v1/chains/mantle-sepolia/status");
        mantleStatus = payload;
        document.getElementById("dataFreshness").textContent = `Data: ${payload.name} live`;
        document.getElementById("heroBlock").textContent = `Block ${payload.latest_block}`;
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
          renderPaperPositions();
        }
      });
    }

    document.getElementById("loadPair").addEventListener("click", loadPair);
    document.getElementById("runBacktest").addEventListener("click", runBacktest);
    document.getElementById("startPaperTrade").addEventListener("click", startPaperTrade);
    document.getElementById("heroStartTrade").addEventListener("click", () => {
      const signal = alphaSignal();
      document.getElementById("notionalUsd").value =
        document.getElementById("heroNotionalUsd").value;
      document.getElementById("tradeSide").value =
        signal.decision === "RISK OFF" ? "watch" : "paper-buy";
      startPaperTrade();
    });
    document.getElementById("primaryStrategy").addEventListener("change", () => {
      const signal = renderAlphaSignal();
      addAudit("Strategy selected", signal.strategyLabel, signal);
    });
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
    renderPaperPositions();
    renderAlphaSignal();
    renderAuditLog();
    runBacktest();
    checkMantle();
    setInterval(tickPaperMark, 2500);
  </script>
</body>
</html>
"""
