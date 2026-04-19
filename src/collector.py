import yfinance as yf
import pandas as pd
from datetime import datetime

class MarketCollector:
    def __init__(self, symbols):
        self.symbols = symbols

    def fetch_data(self, period="1d"):
        """Fetches market data for the configured symbols over a specific period."""
        data_list = []
        
        for symbol in self.symbols:
            print(f"Fetching {period} data for {symbol}...")
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if not hist.empty:
                for date, row in hist.iterrows():
                    data_list.append({
                        'symbol': symbol,
                        'price': row['Close'],
                        'volume': int(row['Volume']) if not pd.isna(row['Volume']) else 0,
                        'timestamp': date,
                        'data_source': 'Yahoo Finance'
                    })
        
        return pd.DataFrame(data_list)

    def fetch_exchange_rates(self, pairs, period="1d"):
        """Fetches exchange rates over a specific period."""
        rates_list = []
        
        for pair in pairs:
            print(f"Fetching {period} rate for {pair}...")
            ticker = yf.Ticker(pair)
            hist = ticker.history(period=period)
            
            if not hist.empty:
                for date, row in hist.iterrows():
                    base = pair[:3]
                    target = pair[3:6]
                    rates_list.append({
                        'base_currency': base,
                        'target_currency': target,
                        'rate': row['Close'],
                        'timestamp': date
                    })
        
        return pd.DataFrame(rates_list)
