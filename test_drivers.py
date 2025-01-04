import pyodbc
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_drivers():
    try:
        drivers = pyodbc.drivers()
        logger.info("Available ODBC drivers:")
        for driver in drivers:
            logger.info(f"- {driver}")
        
        if 'ODBC Driver 17 for SQL Server' in drivers:
            logger.info("Required SQL Server driver is installed!")
        else:
            logger.warning("Required SQL Server driver is NOT installed!")
            
    except Exception as e:
        logger.error(f"Error checking drivers: {e}")

if __name__ == "__main__":
    check_drivers()