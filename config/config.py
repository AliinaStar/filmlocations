from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging
from urllib.parse import quote_plus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

Base = declarative_base()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

required_env_vars = ['DB_USER', 'DB_PASS', 'DB_HOST', 'DB_NAME']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Ensure the driver name matches the installed ODBC driver
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={DB_HOST};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASS};"
)

def get_engine():
    try:
        encoded_connection_string = quote_plus(connection_string)
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={encoded_connection_string}")
        with engine.connect() as connection:
            logger.info("Database connection successful!")
        return engine
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

engine = get_engine()

SessionLocal = sessionmaker(autocommit=False, 
                          autoflush=False, 
                          bind=engine)

def init_db():
    """Ініціалізація бази даних"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def get_db():
    """Функція для отримання сесії бази даних"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()