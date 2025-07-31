# storage/startup.py
from loguru import logger
import time
from sqlalchemy.exc import OperationalError
from storage.db import engine, Base

MAX_RETRIES = 10
RETRY_DELAY = 2

def initialize_database():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            logger.info("Trying to connect to the database...")
            Base.metadata.create_all(bind=engine)
            logger.success("Database initialized.")
            return
        except OperationalError as e:
            retries += 1
            logger.warning(f"Database connection failed: {e}")
            logger.info(f"Retrying in {RETRY_DELAY} seconds... ({retries}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)

    logger.critical("Failed to initialize the database after multiple attempts.")
    raise Exception("Database init failed")
