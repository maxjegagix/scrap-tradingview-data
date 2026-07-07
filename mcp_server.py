#!/usr/bin/env python3
"""
TradingView Data Scraper MCP Server
Integrates with Claude/Hermes agent via Model Context Protocol
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from main import fetch_trading_data, save_to_json, save_to_csv

class TradingViewMCPServer:
    """MCP Server for TradingView Data Scraper"""
    
    def __init__(self):
        self.tools = {
            "fetch_trading_data": self.handle_fetch_trading_data,
            "get_last_hour": self.handle_get_last_hour,
            "get_last_day": self.handle_get_last_day,
            "get_last_week": self.handle_get_last_week,
        }
    
    def handle_fetch_trading_data(self, params):
        """
        Fetch trading data for any symbol
        
        Args:
            symbol: Trading symbol (e.g., "XAUUSD", "AAPL", "EURUSD")
            timeframe: Timeframe in minutes (e.g., "1", "5", "15", "60", "D")
            candles: Number of candles to fetch
        
        Returns:
            dict: Candle data and summary
        """
        symbol = params.get("symbol", "XAUUSD")
        timeframe = params.get("timeframe", "1")
        candles = params.get("candles", 5000)
        
        try:
            data = fetch_trading_data(symbol=symbol, timeframe=timeframe, candles=int(candles))
            
            # Save files
            json_file = save_to_json(data, symbol, timeframe)
            csv_file = save_to_csv(data, symbol, timeframe)
            
            # Calculate summary
            if data:
                values = [candle['v'] for candle in data]
                summary = {
                    "total_candles": len(data),
                    "open": values[0][1],
                    "close": values[-1][4],
                    "high": max(v[2] for v in values),
                    "low": min(v[3] for v in values),
                    "avg_volume": sum(v[5] for v in values) / len(values),
                    "json_file": json_file,
                    "csv_file": csv_file,
                }
            else:
                summary = {"error": "No data retrieved"}
            
            return {
                "status": "success",
                "symbol": symbol,
                "timeframe": timeframe,
                "summary": summary,
                "data": data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def handle_get_last_hour(self, params):
        """Get last 1 hour of data (M5 candles = 12 candles)"""
        symbol = params.get("symbol", "XAUUSD")
        return self.handle_fetch_trading_data({
            "symbol": symbol,
            "timeframe": "5",
            "candles": 12
        })
    
    def handle_get_last_day(self, params):
        """Get last 24 hours of data (M1 candles = 1440 candles)"""
        symbol = params.get("symbol", "XAUUSD")
        return self.handle_fetch_trading_data({
            "symbol": symbol,
            "timeframe": "1",
            "candles": 1440
        })
    
    def handle_get_last_week(self, params):
        """Get last 7 days of data (Daily candles = 7 candles)"""
        symbol = params.get("symbol", "XAUUSD")
        return self.handle_fetch_trading_data({
            "symbol": symbol,
            "timeframe": "D",
            "candles": 7
        })
    
    def process_request(self, request):
        """Process incoming MCP request"""
        tool = request.get("tool")
        params = request.get("params", {})
        
        if tool not in self.tools:
            return {
                "status": "error",
                "message": f"Unknown tool: {tool}",
                "available_tools": list(self.tools.keys())
            }
        
        return self.tools[tool](params)


def main():
    """Main MCP server entry point - handles both stdin and direct calls"""
    import sys
    
    server = TradingViewMCPServer()
    
    # If arguments provided, process as direct call
    if len(sys.argv) > 1:
        try:
            request = json.loads(sys.argv[1])
            response = server.process_request(request)
            print(json.dumps(response, indent=2))
            return
        except json.JSONDecodeError as e:
            print(json.dumps({"status": "error", "message": str(e)}))
            return
        except Exception as e:
            print(json.dumps({"status": "error", "message": str(e)}))
            return
    
    # Otherwise read from stdin
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                request = json.loads(line)
                response = server.process_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                error_response = {"status": "error", "message": f"Invalid JSON: {str(e)}"}
                print(json.dumps(error_response))
                sys.stdout.flush()
            except Exception as e:
                error_response = {"status": "error", "message": str(e)}
                print(json.dumps(error_response))
                sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass


if __name__ == "__main__":
    main()

