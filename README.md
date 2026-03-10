# BTC Backtesting App

## Setup
```bash
cd agents/quant
pip install --user -r requirements.txt  # if needed
```

## Update Data
```bash
python3 update_data.py --all  # Fetch/append latest data
```

## Run Backtest
```bash
python3 backtest.py --tf 1d --strategy sma  # Examples: rsi, macd
```
Outputs metrics (Sharpe, Drawdown, Win Rate) and saves PNG equity curve.

Data in `data/btc-*.csv` (2018-present).
