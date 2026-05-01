# Market service - fetch USD/EUR/Gold/Oil prices
import requests
from config import Config
from utils.logger import logger
from services.cache_service import cache_service
from datetime import datetime

TGJU_API = "https://api.tgju.org/v1/market/indicator/summary-table-data"
YAHOO_API = "https://query1.finance.yahoo.com/v8/finance/chart"
HEADERS = {"User-Agent": "Mozilla/5.0"}


class TGJUService:
    """Service for fetching prices from TGJU API"""

    @staticmethod
    def _fetch_tgju(symbol: str) -> float | None:
        """Fetch latest price for a TGJU symbol"""
        try:
            r = requests.get(f"{TGJU_API}/{symbol}", timeout=Config.REQUEST_TIMEOUT)
            r.raise_for_status()  # Check HTTP status
            data = r.json()
            raw = data["data"][0][0]  # latest row, first column
            return float(raw.replace(",", ""))
        except Exception as e:
            logger.error(f"TGJU fetch error ({symbol}): {e}")
            return None

    @staticmethod
    def get_usd_to_irr() -> dict:
        cached = cache_service.get("usd_irr")
        if cached:
            return cached
        logger.info("Fetching USD/IRR from TGJU...")
        price = TGJUService._fetch_tgju("price_dollar_rl")
        if price is None:
            return None
        result = {"asset": "USD", "price": price, "currency": "IRR",
                  "timestamp": datetime.utcnow().isoformat(), "source": "TGJU"}
        cache_service.set("usd_irr", result, Config.USD_IRR_CACHE_MINUTES)
        logger.info(f"USD/IRR fetched: {price}")
        return result

    @staticmethod
    def get_eur_to_irr() -> dict:
        cached = cache_service.get("eur_irr")
        if cached:
            return cached
        logger.info("Fetching EUR/IRR from TGJU...")
        price = TGJUService._fetch_tgju("price_eur")
        if price is None:
            return None
        result = {"asset": "EUR", "price": price, "currency": "IRR",
                  "timestamp": datetime.utcnow().isoformat(), "source": "TGJU"}
        cache_service.set("eur_irr", result, Config.EUR_IRR_CACHE_MINUTES)
        logger.info(f"EUR/IRR fetched: {price}")
        return result

    @staticmethod
    def get_gold_price() -> dict:
        cached = cache_service.get("gold_price")
        if cached:
            return cached
        logger.info("Fetching Gold price from TGJU...")
        price = TGJUService._fetch_tgju("sekee")  # Emami gold coin
        if price is None:
            return None
        result = {"asset": "Gold Coin", "price": price, "currency": "IRR",
                  "timestamp": datetime.utcnow().isoformat(), "source": "TGJU"}
        cache_service.set("gold_price", result, Config.GOLD_CACHE_MINUTES)
        logger.info(f"Gold price fetched: {price}")
        return result


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