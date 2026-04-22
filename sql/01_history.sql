-- Table for detailed financial historical data (optimized for GoFin)
CREATE TABLE IF NOT EXISTS historical_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date TIMESTAMP NOT NULL,
    open DECIMAL(18, 6),
    high DECIMAL(18, 6),
    low DECIMAL(18, 6),
    close DECIMAL(18, 6),
    adj_close DECIMAL(18, 6),
    volume BIGINT,
    UNIQUE(symbol, date)
);

-- Index for performance
CREATE INDEX IF NOT EXISTS idx_symbol_date ON historical_prices(symbol, date);
