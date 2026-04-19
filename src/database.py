import os
from sqlalchemy import create_engine
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
