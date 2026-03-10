#!/usr/bin/env python3
import sys
import os
import pandas as pd
import ccxt
from datetime import datetime
import argparse

# Add user site-packages
sys.path.insert(0, '/home/clawbox/.local/lib/python3.10/site-packages')

def fetch_and_save(tf, symbol='BTC/USDT', since_str='2018-01-01'):
    exchange = ccxt.binance()
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    csv_file = os.path.join(data_dir, f'btc-{tf}.csv')
    
    since = int(datetime.strptime(since_str, '%Y-%m-%d').timestamp() * 1000)
    
    # If file exists, get last timestamp
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        last_ts = pd.to_datetime(df['timestamp'].iloc[-1]).timestamp() * 1000
        since = int(last_ts) + 1  # next candle
        print(f"Appending from {pd.to_datetime(since, unit='ms')}")
    else:
        print(f"Fetching from {pd.to_datetime(since, unit='ms')}")
    
    all_ohlcv = []
    while True:
        ohlcv = exchange.fetch_ohlcv(symbol, tf, since=since, limit=1000)
        if not ohlcv:
            break
        all_ohlcv.extend(ohlcv)
        since = ohlcv[-1][0] + 1
        print(f"Fetched {len(ohlcv)} candles up to {pd.to_datetime(ohlcv[-1][0], unit='ms')}")
    
    if all_ohlcv:
        df_new = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df_new['timestamp'] = pd.to_datetime(df_new['timestamp'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
        df_new = df_new.astype({'open': float, 'high': float, 'low': float, 'close': float, 'volume': float})
        
        if os.path.exists(csv_file):
            df_old = pd.read_csv(csv_file)
            df = pd.concat([df_old, df_new]).drop_duplicates('timestamp').sort_values('timestamp')
        else:
            df = df_new
        
        df.to_csv(csv_file, index=False)
        print(f"Saved {len(df)} rows to {csv_file}")
    else:
        print(f"No new data for {tf}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true', help='Update all timeframes')
    parser.add_argument('--tf', help='Specific timeframe: 4h,1d,1w')
    args = parser.parse_args()
    
    timeframes = ['4h', '1d', '1w'] if args.all else [args.tf]
    
    for tf in timeframes:
        fetch_and_save(tf)
