# AutoDataWareHouse 📊🚀

AutoDataWareHouse is a modern, automated Data Warehouse (DWH) designed to fetch, process, and store global market data. Built with Python, PostgreSQL (Supabase), and GitHub Actions, it provides a seamless data pipeline for financial analysis and visualization.

## 🌟 Key Features
- **Automated ETL Pipeline**: Daily extraction and full historical sync (up to 5 years).
- **GoFin Ready**: Specifically optimized for the GoFin project, tracking the Top 30 global assets (AAPL, NVDA, BTC, etc.) with high-precision OHLCV data.
- **Auto-Migrations**: Integrated schema management that automatically updates the database (Supabase/Docker) without manual SQL execution.
- **Global Asset Coverage**: Monitors 30+ core assets including Tech Stocks, Crypto, Commodities, and Indices.
- **CI/CD Automation**: Scheduled updates via **GitHub Actions** with manual trigger support for different sync modes.
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
2. Start the local database: `docker-compose up -d`.
3. Install dependencies: `pip install -r requirements.txt`.
4. **Initialize/Migrate Database**:
   ```bash
   python src/migrate.py
   ```
5. Run the ETL process (available modes: `daily` or `history`):
   ```bash
   python src/main.py history
   ```

### 2. GitHub Actions Automation
To automate daily updates and migrations:
1. Configure `DATABASE_URL` in **Settings > Secrets and variables > Actions**.
2. Trigger manually via **Actions > Daily Data Update > Run workflow**.
   - Input `mode: daily` for nightly updates.
   - Input `mode: history` for a full 5-year sync.

## 📊 Data Schema
- `historical_prices`: High-precision OHLCV data (Open, High, Low, Close, Adjusted Close, Volume) for the Top 30 tracked assets. Optimized for **GoFin**.
- `market_data`: General price and volume tracking for diverse assets.
- `exchange_rates`: Nightly exchange rates for major currency pairs.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Created by [MichelBernasconi](https://github.com/MichelBernasconi)*