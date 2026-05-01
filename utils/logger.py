# Logging configuration for debugging and monitoring
import logging
import os
from config import Config

# Create logs directory if not exists
os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

# Configure logging format
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)