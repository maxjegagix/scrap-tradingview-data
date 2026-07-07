---
name: tradingview-data-scraper
description: Fetch real market data from TradingView for stocks, forex, commodities, and cryptocurrencies
version: 1.0.0
author: Trading Data Agent
tags:
  - trading
  - market-data
  - financial
  - stocks
  - forex
  - cryptocurrencies
  - commodities

capabilities:
  - Fetch OHLCV candle data for any trading symbol
  - Support multiple timeframes (1m to monthly)
  - Export to JSON and CSV formats
  - Quick access to last hour/day/week data
  - Real market data from TradingView

tools:
  - name: fetch_trading_data
    description: Fetch trading data for any symbol with custom parameters
    parameters:
      symbol:
        type: string
        description: Trading symbol (e.g., XAUUSD, AAPL, EURUSD, BTCUSD)
        required: true
        example: XAUUSD
      timeframe:
        type: string
        description: Timeframe in minutes or D/W/M (1, 5, 15, 30, 60, 240, D, W, M)
        required: true
        default: "1"
        example: "5"
      candles:
        type: integer
        description: Number of historical candles to fetch
        required: true
        default: 5000
        example: 100
    returns:
      type: object
      properties:
        status: success|error
        symbol: string
        timeframe: string
        summary:
          total_candles: integer
          open: number
          close: number
          high: number
          low: number
          avg_volume: number
          json_file: string
          csv_file: string

  - name: get_last_hour
    description: Fetch last 1 hour of data (M5 candles)
    parameters:
      symbol:
        type: string
        description: Trading symbol
        required: true
        example: XAUUSD
    returns:
      type: object
      properties:
        status: success|error
        summary: object
        data: array

  - name: get_last_day
    description: Fetch last 24 hours of data (M1 candles)
    parameters:
      symbol:
        type: string
        description: Trading symbol
        required: true
        example: EURUSD
    returns:
      type: object
      properties:
        status: success|error
        summary: object
        data: array

  - name: get_last_week
    description: Fetch last 7 days of data (Daily candles)
    parameters:
      symbol:
        type: string
        description: Trading symbol
        required: true
        example: AAPL
    returns:
      type: object
      properties:
        status: success|error
        summary: object
        data: array

examples:
  - description: Get last hour of gold prices
    request:
      tool: get_last_hour
      params:
        symbol: XAUUSD
    response:
      status: success
      summary:
        total_candles: 12
        high: 4140.35
        low: 4124.53

  - description: Get custom timeframe data
    request:
      tool: fetch_trading_data
      params:
        symbol: AAPL
        timeframe: "60"
        candles: 100
    response:
      status: success
      summary:
        total_candles: 100
        open: 290.24
        close: 298.76

symbols_reference:
  stocks:
    - AAPL
    - MSFT
    - GOOGL
    - TSLA
    - NVDA
    - META
  forex:
    - EURUSD
    - GBPUSD
    - USDJPY
    - AUDUSD
    - USDCAD
  commodities:
    - XAUUSD
    - XAGUSD
    - USOIL
    - NATGAS
  crypto:
    - BTCUSD
    - ETHUSD
    - LTCUSD
    - XRPUSD
    - ADAUSD

configuration:
  data_folder: ./data
  json_export: true
  csv_export: true
  auto_organize: true
  max_candles: 10000
