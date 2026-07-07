#!/usr/bin/env python3
"""
Simple wrapper to call MCP server tools directly
Usage: python call_mcp.py <tool> <symbol> [timeframe] [candles]
"""

import sys
import json
from mcp_server import TradingViewMCPServer

def main():
    if len(sys.argv) < 3:
        print("Usage: python call_mcp.py <tool> <symbol> [timeframe] [candles]")
        print("\nTools:")
        print("  - get_last_hour <symbol>")
        print("  - get_last_day <symbol>")
        print("  - get_last_week <symbol>")
        print("  - fetch <symbol> <timeframe> <candles>")
        print("\nExamples:")
        print("  python call_mcp.py get_last_hour XAUUSD")
        print("  python call_mcp.py fetch AAPL 60 100")
        sys.exit(1)
    
    server = TradingViewMCPServer()
    tool = sys.argv[1]
    symbol = sys.argv[2]
    
    request = None
    
    if tool == "get_last_hour":
        request = {"tool": "get_last_hour", "params": {"symbol": symbol}}
    elif tool == "get_last_day":
        request = {"tool": "get_last_day", "params": {"symbol": symbol}}
    elif tool == "get_last_week":
        request = {"tool": "get_last_week", "params": {"symbol": symbol}}
    elif tool == "fetch":
        if len(sys.argv) < 5:
            print("Usage: python call_mcp.py fetch <symbol> <timeframe> <candles>")
            sys.exit(1)
        request = {
            "tool": "fetch_trading_data",
            "params": {
                "symbol": symbol,
                "timeframe": sys.argv[3],
                "candles": int(sys.argv[4])
            }
        }
    else:
        print(f"Unknown tool: {tool}")
        sys.exit(1)
    
    response = server.process_request(request)
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
