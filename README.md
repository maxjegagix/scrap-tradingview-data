# TradingView Data Scraper

A Python utility to fetch real market data from TradingView for any trading symbol, currency pair, commodity, or cryptocurrency.

## Features

- ✅ **Real Market Data** - Fetch actual OHLCV (Open, High, Low, Close, Volume) data from TradingView
- ✅ **Multi-Universe Support** - Stocks, Forex, Commodities, Cryptocurrencies
- ✅ **Flexible Timeframes** - 1-minute to daily candles
- ✅ **Multiple Export Formats** - JSON and CSV
- ✅ **Data Summary** - Quick statistics (High, Low, Average Volume)
- ✅ **Customizable Parameters** - Symbol, timeframe, and candle count

## Installation

### Prerequisites
- Python 3.11+
- pip or uv package manager

### Setup

```bash
# Navigate to project directory
cd scrap-tradingview-data

# Activate virtual environment (if using .venv)
.venv\Scripts\activate

# Install dependencies
pip install tradingview-websocket
```

## Usage

### Basic Command Structure

```bash
python main.py [SYMBOL] [TIMEFRAME] [CANDLES]
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `SYMBOL` | string | `XAUUSD` | Trading symbol/pair (case-sensitive) |
| `TIMEFRAME` | string | `1` | Timeframe in minutes (1, 5, 15, 60) or 'D' for daily |
| `CANDLES` | integer | `5000` | Number of historical candles to fetch |

---

## Examples

### Stocks

```bash
# Apple - 1 minute, 100 candles
python main.py AAPL 1 100

# Microsoft - 1 hour, 250 candles
python main.py MSFT 60 250

# Tesla - 15 minutes, 500 candles
python main.py TSLA 15 500

# S&P 500 Index - Daily, 365 candles (1 year)
python main.py SPX D 365

# Nasdaq 100 - 5 minutes, 1000 candles
python main.py NDX 5 1000

# Google - 4 hours (240 min), 100 candles
python main.py GOOGL 240 100
```

### Forex (Currency Pairs)

```bash
# EUR/USD - 1 minute, 1000 candles
python main.py EURUSD 1 1000

# GBP/USD - 15 minutes, 500 candles
python main.py GBPUSD 15 500

# USD/JPY - 1 hour, 200 candles
python main.py USDJPY 60 200

# AUD/USD - 5 minutes, 2000 candles
python main.py AUDUSD 5 2000

# EUR/GBP - Daily, 250 candles
python main.py EURGBP D 250

# USD/CAD - 30 minutes, 800 candles
python main.py USDCAD 30 800
```

### Commodities

```bash
# Gold (XAUUSD) - 1 minute, 5000 candles
python main.py XAUUSD 1 5000

# Silver (XAGUSD) - 15 minutes, 2000 candles
python main.py XAGUSD 15 2000

# Oil (WTI Crude) - 1 hour, 500 candles
python main.py USOIL 60 500

# Natural Gas - Daily, 365 candles
python main.py NATGAS D 365

# Copper - 5 minutes, 1500 candles
python main.py COPPER 5 1500
```

### Cryptocurrencies

```bash
# Bitcoin - 1 minute, 2000 candles
python main.py BTCUSD 1 2000

# Ethereum - 15 minutes, 1000 candles
python main.py ETHUSD 15 1000

# Bitcoin (from Coinbase) - 5 minutes, 500 candles
python main.py BTCUSD 5 500

# Litecoin - 1 hour, 200 candles
python main.py LTCUSD 60 200

# Ripple - Daily, 100 candles
python main.py XRPUSD D 100

# Cardano - 30 minutes, 800 candles
python main.py ADAUSD 30 800
```

### Default Behavior

```bash
# Uses default: XAUUSD, 1 minute, 5000 candles
python main.py
```

---

## Timeframe Values

| Value | Description |
|-------|-------------|
| `1` | 1-minute candle |
| `5` | 5-minute candle |
| `15` | 15-minute candle |
| `30` | 30-minute candle |
| `60` | 1-hour candle |
| `240` | 4-hour candle |
| `D` or `1D` | Daily candle |
| `W` or `1W` | Weekly candle |
| `M` or `1M` | Monthly candle |

---

## Output

### Generated Files

Each run generates two files with timestamps:

```
data_SYMBOL_TIMEFRAMEm_YYYYMMDDhhmmss.json
data_SYMBOL_TIMEFRAMEm_YYYYMMDDhhmmss.csv
```

**Example:**
```
data_EURUSD_15m_20260707_105140.json
data_EURUSD_15m_20260707_105140.csv
```

### CSV Format

Clean, spreadsheet-friendly format:

```csv
Index,Timestamp,Open,High,Low,Close,Volume
0,2026-07-06 22:30:00,1.14178,1.14238,1.14166,1.14233,1220
1,2026-07-06 22:45:00,1.14234,1.14262,1.14227,1.14253,1157
2,2026-07-06 23:00:00,1.14254,1.14286,1.1425,1.14264,877
```

### JSON Format

Complete data structure for programmatic access:

```json
[
  {
    "i": 0,
    "v": [1783381800.0, 4163.505, 4163.665, 4162.36, 4163.59, 379.0]
  },
  {
    "i": 1,
    "v": [1783381860.0, 4163.55, 4163.62, 4161.925, 4162.505, 261.0]
  }
]
```

### Console Output

```
Fetching data for EURUSD | Timeframe: 15m | Candles: 50

✓ Fetched 50 candles for EURUSD

============================================================
Summary for EURUSD
============================================================
Total Candles: 50
Open (First):  1.14
Close (Last):  1.14
High (Max):    1.14
Low (Min):     1.14
Avg Volume:    640
============================================================

✓ Data saved to data_EURUSD_15m_20260707_105140.json
✓ Data saved to data_EURUSD_15m_20260707_105140.csv
```

---

## Common Use Cases

### Get Last 24 Hours of Data (1-minute candles)
```bash
python main.py AAPL 1 1440
```
*(1440 = 24 hours × 60 minutes)*

### Get Last Week of Data (Daily candles)
```bash
python main.py EURUSD D 7
```

### Get Last Month of Data (Hourly candles)
```bash
python main.py BTCUSD 60 730
```
*(730 ≈ 1 month × 24 hours)*

### Get Last Year of Data (Daily candles)
```bash
python main.py SPX D 365
```

### Intraday Trading Data (5-min, 2000 candles)
```bash
python main.py XAUUSD 5 2000
```

---

## Symbol Reference

### Popular Stocks
- `AAPL` - Apple
- `MSFT` - Microsoft
- `GOOGL` - Google
- `AMZN` - Amazon
- `TSLA` - Tesla
- `NVDA` - NVIDIA
- `META` - Meta (Facebook)

### Major Indices
- `SPX` - S&P 500
- `NDX` - Nasdaq 100
- `INDU` - Dow Jones Industrial Average
- `VIX` - Volatility Index

### Major Forex Pairs
- `EURUSD` - Euro/US Dollar
- `GBPUSD` - British Pound/US Dollar
- `USDJPY` - US Dollar/Japanese Yen
- `AUDUSD` - Australian Dollar/US Dollar
- `USDCAD` - US Dollar/Canadian Dollar
- `NZDUSD` - New Zealand Dollar/US Dollar
- `EURGBP` - Euro/British Pound

### Commodities
- `XAUUSD` - Gold
- `XAGUSD` - Silver
- `USOIL` - WTI Crude Oil
- `NATGAS` - Natural Gas
- `COPPER` - Copper

### Cryptocurrencies
- `BTCUSD` - Bitcoin
- `ETHUSD` - Ethereum
- `LTCUSD` - Litecoin
- `XRPUSD` - Ripple
- `ADAUSD` - Cardano
- `DOGEUSD` - Dogecoin

---

## Troubleshooting

### ModuleNotFoundError: No module named 'tradingview_websocket'

**Solution:** Install the required package
```bash
pip install tradingview-websocket
```

### No data returned

**Solution:** Verify symbol is correct and markets are open for that instrument

### Connection timeout

**Solution:** Check internet connection and try again with fewer candles:
```bash
python main.py SYMBOL TIMEFRAME 100
```

---

## Notes

- **Data Type:** Real historical market data from TradingView
- **Update Frequency:** Historical data, not real-time streaming
- **Rate Limits:** TradingView may have connection limits; avoid excessive rapid requests
- **Accuracy:** Data reflects market activity; volumes are approximate for some instruments

---

## License

MIT License - Feel free to use and modify for your projects

---

## Questions or Issues?

Need help? Check:
1. Symbol name is correct (case-sensitive)
2. Timeframe is supported (1, 5, 15, 30, 60, 240, D, W, M)
3. Internet connection is active
4. Market is open for the selected instrument

Enjoy fetching your trading data! 📈
