# TradingView Data Scraper - MCP/Hermes Agent Integration

This document explains how to integrate the TradingView Data Scraper as an MCP server or skill in the Hermes agent.

## Quick Start

### Option 1: Use as MCP Server (Claude/Hermes)

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
# or
uv pip install tradingview-websocket websocket-client
```

#### 2. Configure MCP Server

Add to your Claude/Hermes configuration:

```json
{
  "mcp_servers": {
    "tradingview": {
      "command": "python",
      "args": ["path/to/mcp_server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

#### 3. Test Connection

```bash
python mcp_server.py
# Send JSON request via stdin:
{"tool": "get_last_hour", "params": {"symbol": "XAUUSD"}}
```

### Option 2: Use as Hermes Agent Skill

#### 1. Place in Hermes Skills Directory

```
~/.hermes/skills/tradingview-data-scraper/
├── SKILL.md
├── main.py
├── mcp_server.py
└── requirements.txt
```

#### 2. Hermes will automatically discover the skill from `SKILL.md`

#### 3. Use in Agent

```
@tradingview fetch XAUUSD on M5 for last hour
@tradingview get AAPL daily data for 365 days
```

---

## Tool Reference

### 1. `fetch_trading_data`

Fetch trading data with custom parameters.

**Parameters:**
- `symbol` (string, required): Trading symbol (e.g., "XAUUSD", "AAPL")
- `timeframe` (string, optional): "1", "5", "15", "60", "D", "W", "M" (default: "1")
- `candles` (integer, optional): Number of candles (default: 5000)

**Example:**
```json
{
  "tool": "fetch_trading_data",
  "params": {
    "symbol": "EURUSD",
    "timeframe": "15",
    "candles": 200
  }
}
```

**Response:**
```json
{
  "status": "success",
  "symbol": "EURUSD",
  "timeframe": "15",
  "summary": {
    "total_candles": 200,
    "open": 1.14234,
    "close": 1.14362,
    "high": 1.14428,
    "low": 1.14178,
    "avg_volume": 850,
    "json_file": "data/json/data_EURUSD_15m_20260707_105140.json",
    "csv_file": "data/csv/data_EURUSD_15m_20260707_105140.csv"
  },
  "data": [...]
}
```

---

### 2. `get_last_hour`

Quick fetch of last 1 hour (M5 candles = 12 candles).

**Parameters:**
- `symbol` (string, required): Trading symbol

**Example:**
```json
{
  "tool": "get_last_hour",
  "params": {
    "symbol": "XAUUSD"
  }
}
```

---

### 3. `get_last_day`

Quick fetch of last 24 hours (M1 candles = 1440 candles).

**Parameters:**
- `symbol` (string, required): Trading symbol

**Example:**
```json
{
  "tool": "get_last_day",
  "params": {
    "symbol": "AAPL"
  }
}
```

---

### 4. `get_last_week`

Quick fetch of last 7 days (Daily candles).

**Parameters:**
- `symbol` (string, required): Trading symbol

**Example:**
```json
{
  "tool": "get_last_week",
  "params": {
    "symbol": "BTCUSD"
  }
}
```

---

## Supported Symbols

### Stocks
AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, IBM, ORCL, INTC

### Indices
SPX (S&P 500), NDX (Nasdaq 100), INDU (Dow Jones)

### Forex Pairs
EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, EURGBP, NZDUSD, GBPJPY

### Commodities
XAUUSD (Gold), XAGUSD (Silver), USOIL (WTI Oil), NATGAS (Natural Gas), COPPER

### Cryptocurrencies
BTCUSD, ETHUSD, LTCUSD, XRPUSD, ADAUSD, DOGEUSD, SOLUSD

---

## Timeframe Values

| Value | Description |
|-------|-------------|
| `1` | 1-minute |
| `5` | 5-minute |
| `15` | 15-minute |
| `30` | 30-minute |
| `60` | 1-hour |
| `240` | 4-hour |
| `D` | Daily |
| `W` | Weekly |
| `M` | Monthly |

---

## Output Files

All exports are automatically organized:

```
data/
├── json/
│   ├── data_XAUUSD_5m_20260707_105852.json
│   ├── data_AAPL_60m_20260707_110000.json
│   └── ...
└── csv/
    ├── data_XAUUSD_5m_20260707_105852.csv
    ├── data_AAPL_60m_20260707_110000.csv
    └── ...
```

### JSON Format
```json
[
  {
    "i": 0,
    "v": [1783381800.0, 4163.505, 4163.665, 4162.36, 4163.59, 379.0]
  }
]
```

### CSV Format
```
Index,Timestamp,Open,High,Low,Close,Volume
0,2026-07-07 10:00:00,4163.505,4163.665,4162.36,4163.59,379
```

---

## Integration Examples

### Claude API Integration

```python
import json
import subprocess

def call_tradingview_tool(tool, params):
    """Call TradingView MCP tool"""
    process = subprocess.Popen(
        ["python", "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    request = json.dumps({"tool": tool, "params": params})
    output, error = process.communicate(request.encode())
    
    return json.loads(output.decode())

# Usage
result = call_tradingview_tool("get_last_hour", {"symbol": "XAUUSD"})
print(result)
```

### Hermes Agent Integration

Create `.hermes-agent.md`:

```markdown
# TradingView Data Scraper Agent

You have access to the TradingView Data Scraper skill for fetching real market data.

## Available Commands

- Fetch last hour: `@tradingview get_last_hour SYMBOL`
- Fetch last day: `@tradingview get_last_day SYMBOL`
- Fetch last week: `@tradingview get_last_week SYMBOL`
- Custom fetch: `@tradingview fetch SYMBOL TIMEFRAME CANDLES`

## Examples

User: "Get me the last hour of gold prices"
Agent: @tradingview get_last_hour XAUUSD

User: "I need Apple stock data for the last 100 1-hour candles"
Agent: @tradingview fetch AAPL 60 100
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tradingview_websocket'"

**Solution:**
```bash
pip install tradingview-websocket
# or
uv pip install tradingview-websocket
```

### Issue: MCP server not responding

**Solution:** Check if the server is running:
```bash
python mcp_server.py
echo '{"tool": "get_last_hour", "params": {"symbol": "XAUUSD"}}' | python mcp_server.py
```

### Issue: No data returned

**Solution:** Verify the symbol is correct and markets are open for that instrument.

---

## Performance Tips

- Use pre-calculated candle counts for common timeframes
- Last hour (M5) = 12 candles
- Last day (M1) = 1440 candles
- Last week (D) = 7 candles
- Last month (H1) ≈ 730 candles

---

## Security Notes

- MCP server reads from stdin and writes to stdout
- No authentication required (run locally)
- Data files are saved to local `data/` directory
- No external API keys needed (uses TradingView web socket)

---

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Test MCP server: `python mcp_server.py`
3. Configure in your agent platform
4. Start fetching market data!

For more information, see `README.md`
