# core/logger.py
from loguru import logger
import sys

# Configure Loguru
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

# Optional: Log to file
logger.add("logs/app.log", rotation="1 MB", retention="7 days", compression="zip")

# Usage: from core.logger import logger
