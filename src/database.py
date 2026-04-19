import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    """Returns a SQLAlchemy engine. Prefers DATABASE_URL if available."""
    url = os.getenv("DATABASE_URL")
    
    if not url:
        user = os.getenv("DB_USER", "admin")
        password = os.getenv("DB_PASSWORD", "admin123")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "warehouse")
        url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    
    return create_engine(url)

def insert_on_conflict_nothing(table, conn, keys, data_iter):
    """
    Custom insert method for pandas.to_sql to handle 'ON CONFLICT DO NOTHING' in Postgres.
    """
    data = [dict(zip(keys, row)) for row in data_iter]
    
    # Get the actual table object from the Metadata
    stmt = insert(table.table).values(data).on_conflict_do_nothing()
    result = conn.execute(stmt)
    return result.rowcount
