# Oil service - fetch oil prices via Yahoo Finance API
import requests
from app.core.config import Config
from app.core.logger import logger
from app.services.price_cache_service import cache_service
from datetime import datetime

YAHOO_API = "https://query1.finance.yahoo.com/v8/finance/chart"
HEADERS = {"User-Agent": "Mozilla/5.0"}


class OilService:
    """Service for oil price data"""

    @staticmethod
    def _fetch_yahoo(symbol: str) -> float | None:
        try:
            r = requests.get(f"{YAHOO_API}/{symbol}", headers=HEADERS,
                             timeout=Config.REQUEST_TIMEOUT)
            r.raise_for_status()  # Check HTTP status
            return r.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]
        except Exception as e:
            logger.error(f"Yahoo Finance fetch error ({symbol}): {e}")
            return None

    @staticmethod
    def get_wti_price() -> dict:
        cached = cache_service.get("wti_oil")
        if cached:
            return cached
        logger.info("Fetching WTI oil price...")
        price = OilService._fetch_yahoo("CL=F")
        if price is None:
            return None
        result = {"asset": "WTI Crude Oil", "symbol": "CL=F", "price_usd": price,
                  "unit": "per barrel", "timestamp": datetime.utcnow().isoformat(),
                  "source": "Yahoo Finance"}
        cache_service.set("wti_oil", result, Config.OIL_CACHE_MINUTES)
        logger.info(f"WTI price fetched: ${price}")
        return result

    @staticmethod
    def get_brent_price() -> dict:
        cached = cache_service.get("brent_oil")
        if cached:
            return cached
        logger.info("Fetching Brent oil price...")
        price = OilService._fetch_yahoo("BZ=F")
        if price is None:
            return None
        result = {"asset": "Brent Crude Oil", "symbol": "BZ=F", "price_usd": price,
                  "unit": "per barrel", "timestamp": datetime.utcnow().isoformat(),
                  "source": "Yahoo Finance"}
        cache_service.set("brent_oil", result, Config.OIL_CACHE_MINUTES)
        logger.info(f"Brent price fetched: ${price}")
        return result