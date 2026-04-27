# Configuration file - stores all settings from environment variables
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Telegram Bot
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8000/webhook")
    
    # SQLite Database for price history and user data
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./marketsnap.db")
    
    # API Endpoints (all free, no keys needed for most)
    TGJU_URL = os.getenv("TGJU_URL", "https://www.tgju.org")
    COINGECKO_URL = os.getenv("COINGECKO_URL", "https://api.coingecko.com/api/v3")
    BINANCE_URL = os.getenv("BINANCE_URL", "https://api.binance.com/api/v3")
    EXCHANGERATE_URL = os.getenv("EXCHANGERATE_URL", "https://exchangerate.host/api")
    
    # Cache settings (TTL in minutes)
    CACHE_TYPE = os.getenv("CACHE_TYPE", "memory")  # redis or memory
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    USD_IRR_CACHE_MINUTES = int(os.getenv("USD_IRR_CACHE_MINUTES", "10"))
    EUR_IRR_CACHE_MINUTES = int(os.getenv("EUR_IRR_CACHE_MINUTES", "10"))
    CRYPTO_CACHE_MINUTES = int(os.getenv("CRYPTO_CACHE_MINUTES", "5"))
    OIL_CACHE_MINUTES = int(os.getenv("OIL_CACHE_MINUTES", "20"))
    GOLD_CACHE_MINUTES = int(os.getenv("GOLD_CACHE_MINUTES", "15"))
    
    # Scheduler update intervals (in minutes)
    TGJU_UPDATE_MINUTES = int(os.getenv("TGJU_UPDATE_MINUTES", "10"))
    CRYPTO_UPDATE_MINUTES = int(os.getenv("CRYPTO_UPDATE_MINUTES", "5"))
    OIL_UPDATE_MINUTES = int(os.getenv("OIL_UPDATE_MINUTES", "20"))
    ALERT_CHECK_MINUTES = int(os.getenv("ALERT_CHECK_MINUTES", "5"))
    
    # API timeouts
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/marketsnap.log")