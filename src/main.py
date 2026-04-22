import sys
from database import get_engine, insert_on_conflict_nothing, Database
from collector import MarketCollector, DataCollector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# Selection of diverse assets for general tracking
SYMBOLS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA',
    'BTC-USD', 'ETH-USD', 'GC=F', '^GSPC'
]

EXCHANGE_PAIRS = [
    'EURUSD=X', 'GBPUSD=X', 'USDJPY=X'
]

def run_etl(mode="daily"):
    print(f"Inizio ETL Process per GoFin (Modalita: {mode})...")
    
    # 1. Market Data & exchange rates (for existing tables)
    collector = MarketCollector(SYMBOLS)
    db = Database()
    
    period = "1d" if mode == "daily" else "1y"
    
    market_df = collector.fetch_data(period=period)
    if not market_df.empty:
        print(f"Loading {len(market_df)} market records...")
        market_df.to_sql('market_data', db.engine, if_exists='append', index=False, method=insert_on_conflict_nothing)
        
    rates_df = collector.fetch_exchange_rates(EXCHANGE_PAIRS, period=period)
    if not rates_df.empty:
        print(f"Loading {len(rates_df)} exchange rate records...")
        rates_df.to_sql('exchange_rates', db.engine, if_exists='append', index=False, method=insert_on_conflict_nothing)

    # 2. Historical Stock Data (Detailed OHLCV for Top 30) - GoFin Logic
    hist_collector = DataCollector()
    # In 'history' mode we take 5 years as requested by GoFin snippet, in 'daily' we take 5 days
    hist_period = "5d" if mode == "daily" else "5y" 
    
    print(f"Scarico dati storici (Periodo: {hist_period})...")
    hist_data = hist_collector.download_data(period=hist_period, interval='1d')
    
    if not hist_data.empty:
        print(f"Scaricati {len(hist_data)} record storico. Inserimento nel DB...")
        # Mapping columns to match historical_prices table
        cols = ['symbol', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
        hist_data = hist_data[[c for c in cols if c in hist_data.columns]]
        
        db.insert_data(hist_data, table_name='historical_prices')
        print("Database popolato con successo!")
    else:
        print("Nessun dato storico scaricato.")
        
    print(f"ETL Process '{mode}' Completato!")

if __name__ == "__main__":
    # Modes: "daily" (default) or "history" (full sync)
    mode = "history" if len(sys.argv) > 1 and sys.argv[1] == "history" else "daily"
    run_etl(mode=mode)
