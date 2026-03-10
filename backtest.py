#!/usr/bin/env python3
import sys
import os
import argparse
import pandas as pd
from datetime import datetime
import backtrader as bt
import matplotlib.pyplot as plt

# Add user site-packages
sys.path.insert(0, '/home/clawbox/.local/lib/python3.10/site-packages')

# Import strategies
from strategies.sma import SMACross
from strategies.rsi import RSIStrategy
from strategies.macd import MACDStrategy

def load_data(tf):
    data_path = f'data/btc-{tf}.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f'{data_path} not found. Run: python3 update_data.py --all')
    
    df = pd.read_csv(data_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    data = bt.feeds.PandasData(dataname=df)
    return data

def run_backtest(tf='1d', strategy='sma', symbol='BTC'):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)  # 0.1% fee

    data = load_data(tf)
    cerebro.adddata(data)

    if strategy == 'sma':
        cerebro.addstrategy(SMACross)
    elif strategy == 'rsi':
        cerebro.addstrategy(RSIStrategy)
    elif strategy == 'macd':
        cerebro.addstrategy(MACDStrategy)
    else:
        raise ValueError(f'Unknown strategy: {strategy}')

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    results = cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Metrics
    strat = results[0]
    sharpe = strat.analyzers.sharpe.get_analysis()
    drawdown = strat.analyzers.drawdown.get_analysis()
    trades = strat.analyzers.trades.get_analysis()
    print('Full Trades Analysis:', trades)

    print(f'Sharpe Ratio: {sharpe.get("sharperatio", "N/A")}')
    print(f'Max Drawdown: {drawdown.get("max", {}).get("drawdown", "N/A"):.2f}%')
    if 'total' in trades:
        total_trades = trades['total']['total']
        won = trades['won']['total']
        win_rate = (won / total_trades * 100) if total_trades > 0 else 0
        print(f'Win Rate: {win_rate:.2f}% ({won}/{total_trades})')

    # Plot
    plot_path = f'backtest_{tf}_{strategy}.png'
    cerebro.plot(style='candlestick', volume=False)
    plt.savefig(plot_path)
    print(f'Equity curve saved to {plot_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tf', default='1d', choices=['4h', '1d', '1w'], help='Timeframe')
    parser.add_argument('--strategy', default='sma', choices=['sma', 'rsi', 'macd'], help='Strategy')
    args = parser.parse_args()
    run_backtest(args.tf, args.strategy)
