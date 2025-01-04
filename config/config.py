from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging
from urllib.parse import quote_plus
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

Base = declarative_base()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

required_env_vars = ['DB_HOST', 'DB_NAME', 'AZURE_CLIENT_ID', 'AZURE_CLIENT_SECRET', 'AZURE_TENANT_ID']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Get the AAD token
try:
    credential = DefaultAzureCredential()
    token = credential.get_token("https://database.windows.net/.default")
except ClientAuthenticationError as e:
    logger.error(f"Authentication error: {e}")
    raise

# Ensure the driver name matches the installed ODBC driver
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={DB_HOST};"
    f"DATABASE={DB_NAME};"
    f"Authentication=ActiveDirectoryServicePrincipal;"
    f"AccessToken={token.token}"
)

def get_engine():
    try:
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}")
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