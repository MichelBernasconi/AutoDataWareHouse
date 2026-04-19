# AutoDataWareHouse 📊🚀

AutoDataWareHouse is a modern, automated Data Warehouse (DWH) designed to fetch, process, and store global market data. Built with Python, PostgreSQL (Supabase), and GitHub Actions, it provides a seamless data pipeline for financial analysis and visualization.

## 🌟 Key Features
- **Automated ETL Pipeline**: Monthly/Daily data extraction from Yahoo Finance.
- **Global Asset Coverage**: Monitors 30+ assets including Tech Stocks (NVDA, AAPL), Crypto (BTC, ETH), Commodities (Gold, Oil), and Indices (S&P500, DAX).
- **Time-Series Management**: Robust schema for handling historical prices and exchange rates.
- **Cloud-Ready**: Fully integrated with **Supabase** for persistent cloud storage.
- **CI/CD Automation**: Scheduled updates via **GitHub Actions** (Data-as-Code approach).
- **Visualization Ready**: Optimized for direct connection with **PowerBI** and **Tableau**.

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **Data Source**: Yahoo Finance (yfinance)
- **Database**: PostgreSQL (Supabase / Local Docker)
- **Infrastructure**: Docker & GitHub Actions
- **Libraries**: Pandas, SQLAlchemy, python-dotenv

## 🚀 Getting Started

### 1. Local Development (Docker)
1. Clone the repository.
2. Start the local database:
   ```bash
   docker-compose up -d
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the ETL process:
   ```bash
   python src/main.py
   ```

### 2. Cloud Setup (Supabase)
1. Create a project on [Supabase](https://supabase.com/).
2. Obtain your **Connection URI** (use the Transaction Pooler for IPv4 compatibility).
3. Set your environment variable:
   ```bash
   DATABASE_URL=your_supabase_uri
   ```

### 3. GitHub Actions Automation
To automate daily updates:
1. Go to your GitHub Repository **Settings > Secrets and variables > Actions**.
2. Add a new secret named `DATABASE_URL` with your connection string.
3. The workflow will run automatically every day at midnight (UTC).

## 📊 Data Schema
- `market_data`: Stores prices, volumes, and timestamps for stocks, crypto, and commodities.
- `exchange_rates`: Stores daily exchange rates for major currency pairs.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Created by [MichelBernasconi](https://github.com/MichelBernasconi)*