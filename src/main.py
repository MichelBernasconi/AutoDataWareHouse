import os
import sys
from database import get_engine, insert_on_conflict_nothing
from collector import MarketCollector
import pandas as pd

# Selection of many diverse assets
SYMBOLS = [
    # Tech
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA',
    # Finance
    'JPM', 'V', 'BAC',
    # Energy & Healthcare
    'XOM', 'CVX', 'PFE', 'JNJ',
    # Crypto
    'BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'XRP-USD',
    # Commodities
    'GC=F', 'SI=F', 'CL=F', 'NG=F',
    # Indices
    '^GSPC', '^DJI', '^IXIC', '^GDAXI', '^FTSE'
]

EXCHANGE_PAIRS = [
    'EURUSD=X', 'GBPUSD=X', 'EURGBP=X', 'USDJPY=X', 'EURJPY=X'
]

def run_etl(period="1d"):
    print(f"Starting ETL Process (Period: {period})...")
    
    # 1. Initialize Collector
    collector = MarketCollector(SYMBOLS)
    engine = get_engine()
    
    # 2. Extract
    market_df = collector.fetch_data(period=period)
    rates_df = collector.fetch_exchange_rates(EXCHANGE_PAIRS, period=period)
    
    # 3. Load
    if not market_df.empty:
        print(f"Loading {len(market_df)} market records to database...")
        # Use custom upsert method to skip existing records (symbol + timestamp)
        market_df.to_sql('market_data', engine, if_exists='append', index=False, method=insert_on_conflict_nothing)
        
    if not rates_df.empty:
        print(f"Loading {len(rates_df)} exchange rate records to database...")
        # Use custom upsert method to skip existing records (base + target + timestamp)
        rates_df.to_sql('exchange_rates', engine, if_exists='append', index=False, method=insert_on_conflict_nothing)
        
    print("ETL Process Completed Successfully!")

if __name__ == "__main__":
    # If "history" is passed as argument, fetch 1 year of data
    period = "1y" if len(sys.argv) > 1 and sys.argv[1] == "history" else "1d"
    run_etl(period=period)
