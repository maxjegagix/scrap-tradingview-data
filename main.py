import sys
import json
import csv
import os
from datetime import datetime
from pathlib import Path
from tradingview_websocket import TradingViewWebSocket

def fetch_trading_data(symbol="XAUUSD", timeframe="1", candles=5000):
    """
    Fetch trading data for any symbol/pair from any universe.
    
    Args:
        symbol (str): Trading symbol (e.g., "XAUUSD", "AAPL", "EURUSD", "BTCUSD")
        timeframe (str): Timeframe in minutes (e.g., "1", "5", "15", "60", "D")
        candles (int): Number of candles to fetch (default: 5000)
    
    Returns:
        dict: Result data containing candles
    """
    print(f"Fetching data for {symbol} | Timeframe: {timeframe}m | Candles: {candles}")
    
    ws = TradingViewWebSocket(
        symbol=symbol,
        timeframe=timeframe,
        candles=candles
    )
    
    ws.connect()
    ws.run()
    
    return ws.result_data

def create_folders():
    """Create data folders if they don't exist."""
    folders = ['data/json', 'data/csv']
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)

def save_to_json(data, symbol, timeframe):
    """Save candle data to JSON file in data/json folder."""
    create_folders()
    filename = f"data/json/data_{symbol}_{timeframe}m_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✓ JSON saved to {filename}")
    return filename

def save_to_csv(data, symbol, timeframe):
    """Save candle data to CSV file in data/csv folder."""
    create_folders()
    filename = f"data/csv/data_{symbol}_{timeframe}m_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Index', 'Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        
        for candle in data:
            idx = candle['i']
            values = candle['v']
            timestamp = datetime.fromtimestamp(values[0]).strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([idx, timestamp, values[1], values[2], values[3], values[4], int(values[5])])
    
    print(f"✓ CSV saved to {filename}")
    return filename

def print_summary(data, symbol):
    """Print data summary."""
    if not data:
        print("No data retrieved")
        return
    
    values = [candle['v'] for candle in data]
    opens = [v[1] for v in values]
    highs = [v[2] for v in values]
    lows = [v[3] for v in values]
    closes = [v[4] for v in values]
    volumes = [v[5] for v in values]
    
    print(f"\n{'='*60}")
    print(f"Summary for {symbol}")
    print(f"{'='*60}")
    print(f"Total Candles: {len(data)}")
    print(f"Open (First):  {opens[0]:.2f}")
    print(f"Close (Last):  {closes[-1]:.2f}")
    print(f"High (Max):    {max(highs):.2f}")
    print(f"Low (Min):     {min(lows):.2f}")
    print(f"Avg Volume:    {sum(volumes)/len(volumes):,.0f}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # Get symbol from command line argument or use default
    symbol = sys.argv[1] if len(sys.argv) > 1 else "XAUUSD"
    timeframe = sys.argv[2] if len(sys.argv) > 2 else "1"
    candles = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
    
    result = fetch_trading_data(symbol=symbol, timeframe=timeframe, candles=candles)
    
    print(f"\n✓ Fetched {len(result)} candles for {symbol}")
    
    # Print summary
    print_summary(result, symbol)
    
    # Save to both JSON and CSV
    save_to_json(result, symbol, timeframe)
    save_to_csv(result, symbol, timeframe)
