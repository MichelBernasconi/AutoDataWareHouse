import os
import sys
from database import get_engine
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
        # Use simple append. Duplicates will be handled by the DB constraint 
        # (or throw an error if we don't handle them, but let's try to be smart)
        try:
            market_df.to_sql('market_data', engine, if_exists='append', index=False)
        except Exception as e:
            print(f"Note: Some records might already exist. ({e})")
            # In a real DWH we would use an Upsert/Merge logic
        
    if not rates_df.empty:
        print(f"Loading {len(rates_df)} exchange rate records to database...")
        try:
            rates_df.to_sql('exchange_rates', engine, if_exists='append', index=False)
        except Exception as e:
            print(f"Note: Some records might already exist. ({e})")
        
    print("ETL Process Completed Successfully!")

if __name__ == "__main__":
    # If "history" is passed as argument, fetch 1 year of data
    period = "1y" if len(sys.argv) > 1 and sys.argv[1] == "history" else "1d"
    run_etl(period=period)
