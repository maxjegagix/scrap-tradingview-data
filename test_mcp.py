#!/usr/bin/env python3
"""
Test script for MCP Server
"""

import json
import subprocess
import sys

def test_mcp_server():
    """Test the MCP server with various requests"""
    
    test_cases = [
        {
            "name": "Get last hour of XAUUSD",
            "request": {"tool": "get_last_hour", "params": {"symbol": "XAUUSD"}}
        },
        {
            "name": "Get last hour of EURUSD",
            "request": {"tool": "get_last_hour", "params": {"symbol": "EURUSD"}}
        },
        {
            "name": "Fetch custom data",
            "request": {"tool": "fetch_trading_data", "params": {"symbol": "AAPL", "timeframe": "60", "candles": 50}}
        }
    ]
    
    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"Test: {test['name']}")
        print(f"{'='*60}")
        print(f"Request: {json.dumps(test['request'], indent=2)}")
        
        try:
            process = subprocess.Popen(
                [sys.executable, "mcp_server.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            request_json = json.dumps(test['request']) + '\n'
            stdout, stderr = process.communicate(input=request_json, timeout=30)
            
            if stdout.strip():
                response = json.loads(stdout.strip())
                print(f"\nResponse Status: {response.get('status')}")
                if response.get('status') == 'success':
                    print(f"Total Candles: {response.get('summary', {}).get('total_candles')}")
                    print(f"High: {response.get('summary', {}).get('high')}")
                    print(f"Low: {response.get('summary', {}).get('low')}")
                    print(f"Files:")
                    print(f"  - JSON: {response.get('summary', {}).get('json_file')}")
                    print(f"  - CSV: {response.get('summary', {}).get('csv_file')}")
                else:
                    print(f"Error: {response.get('message')}")
            
            if stderr.strip():
                print(f"Stderr: {stderr}")
                
        except subprocess.TimeoutExpired:
            print("ERROR: Request timed out")
            process.kill()
        except Exception as e:
            print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_mcp_server()
