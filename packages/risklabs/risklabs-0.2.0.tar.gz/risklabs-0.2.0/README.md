# RiskLabs

**Decision-Risk & Robustness Simulator** by [Eiffel Labs](https://eiffellabs.com/)

RiskLabs is a Python library designed to help quantitative researchers and portfolio managers evaluate the robustness of their strategies. It goes beyond simple backtesting by subjecting strategies to various "flight path" scenarios, such as historical crashes, volatility spikes, and correlation breakdowns.

## Features

-   **Scenario Analysis**: Simulate strategies under stress conditions (e.g., 2008 Crash, COVID-19 Volatility).
-   **Robustness Metrics**: Calculate specialized scores based on performance stability across regimes.
-   **Regime Detection**: Analyze strategy behavior in Bull vs. Bear markets.
-   **HTML Reporting**: Generate beautiful, standalone HTML dashboards with interactive charts.
-   **Privacy-First**: Runs entirely locally. No data leaves your machine.

## Installation

```bash
pip install risklabs
```

## Quick Start

```python
from risklabs.client import create_strategy, analyze

# 1. Define a Strategy
strategy = create_strategy(
    name="My 60/40 Portfolio",
    allocations=[
        {"ticker": "SPY", "weight": 0.6},
        {"ticker": "AGG", "weight": 0.4}
    ]
)

# 2. Run Robustness Analysis
print("Running simulations...")
report = analyze(strategy)

# 3. Generate Report
report.to_file("my_portfolio_report.html")
print("Report generated: my_portfolio_report.html")
```

## How It Works

1.  **Define Strategy**: You specify target allocations (static weights for MVP).
2.  **Fetch Data**: The library automatically downloads historical data for the tickers using `yfinance`.
3.  **Simulate Scenarios**: The engine runs multiple simulations:
    -   *Historical Baseline*: Standard backtest.
    -   *Crash Replay*: Applies historical shock factors.
    -   *Regime Stress*: Modifies volatility and correlation matrices.
4.  **Score & Report**: Aggregates results into a "Robustness Score" and renders an HTML dashboard.

## License

MIT
