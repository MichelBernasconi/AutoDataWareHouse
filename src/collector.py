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

class DataCollector:
    def __init__(self):
        # Lista delle 30 testate per GoFin (S&P 500 Top)
        self.tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 
            'UNH', 'JNJ', 'XOM', 'JPM', 'V', 'PG', 'MA', 'AVGO', 'HD', 'CVX', 
            'MRK', 'ABBV', 'ABT', 'COST', 'PEP', 'ADBE', 'WMT', 'MCD', 'CRM', 
            'PFE', 'BAC', 'BTC-USD'
        ]

    def download_data(self, period='max', interval='1d'):
        """Scarica i dati storici per tutti i tickers selezionati"""
        all_data = []
        for ticker in self.tickers:
            print(f"Scarico dati per {ticker} (Periodo: {period})...")
            try:
                # yf.download is faster for bulk, but let's keep the logic consistent
                df = yf.download(ticker, period=period, interval=interval, auto_adjust=False)
                if df.empty: continue
                
                # Reset index per avere la data come colonna
                df = df.reset_index()
                df['symbol'] = ticker
                
                # Rinomina colonne per matchare il DB
                # yfinance returns: Date, Open, High, Low, Close, Adj Close, Volume
                # Se yfinance restituisce un MultiIndex (es. in versioni recenti), lo appiattiamo
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                df.columns = [str(c).lower().replace(' ', '_') for c in df.columns]
                
                # Rename 'date'/'datetime' to 'date' if needed
                if 'date' not in df.columns and 'datetime' in df.columns:
                    df = df.rename(columns={'datetime': 'date'})
                
                all_data.append(df)
            except Exception as e:
                print(f"Errore su {ticker}: {e}")
        
        return pd.concat(all_data) if all_data else pd.DataFrame()
