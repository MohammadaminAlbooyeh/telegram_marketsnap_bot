# Market service - fetch USD/EUR/Gold/Oil prices
import sys
import os
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from datetime import datetime

from config import Config
from services.cache_service import cache_service
from utils.logger import logger


YAHOO_API = "https://query1.finance.yahoo.com/v8/finance/chart"
HEADERS = {"User-Agent": "Mozilla/5.0"}

TGJU_ENDPOINT_PREFIX = "/v1/market/indicator/summary-table-data"


class TGJUService:
    """Service for fetching prices from TGJU API (with fallback)."""

    @staticmethod
    def _fetch_tgju(symbol: str) -> float | None:
        """Fetch latest price for a TGJU symbol."""
        try:
            tgju_base = Config.TGJU_URL.rstrip("/")
            tgju_api = f"{tgju_base}{TGJU_ENDPOINT_PREFIX}"
            r = requests.get(
                f"{tgju_api}/{symbol}",
                timeout=Config.REQUEST_TIMEOUT,
            )
            r.raise_for_status()
            data = r.json()
            raw = data["data"][0][0]  # latest row, first column
            return float(str(raw).replace(",", ""))
        except Exception as e:
            logger.error(f"TGJU fetch error ({symbol}): {e}")
            return None

    @staticmethod
    def _fetch_exchangerate_to_irr(base: str) -> float | None:
        """Fallback: fetch FX rate to IRR from moneyconvert.net."""
        try:
            url = "https://cdn.moneyconvert.net/api/latest.json"
            r = requests.get(
                url,
                timeout=Config.REQUEST_TIMEOUT,
                headers=HEADERS,
            )
            r.raise_for_status()
            data = r.json()

            rates = data.get("rates", {})

            if base.upper() == "USD":
                # Direct USD to IRR
                irr_rate = rates.get("IRR")
                if irr_rate is not None and irr_rate > 0:
                    return float(irr_rate)
            elif base.upper() == "EUR":
                # EUR to IRR: calculate via USD
                # Get USD/IRR rate
                usd_to_irr = rates.get("IRR")
                if usd_to_irr is None or usd_to_irr <= 0:
                    return None

                # Get EUR/USD rate
                eur_to_usd = rates.get("EUR")
                if eur_to_usd is None or eur_to_usd == 0:
                    return None

                # EUR to IRR = USD to IRR / EUR to USD
                return usd_to_irr / eur_to_usd

            return None
        except Exception as e:
            logger.error(f"MoneyConvert fallback fetch error ({base}->IRR): {e}")
            return None

    @staticmethod
    def get_usd_to_irr() -> dict | None:
        cached = cache_service.get("usd_irr")
        if cached:
            return cached

        logger.info("Fetching USD/IRR from TGJU...")
        price = TGJUService._fetch_tgju("price_dollar_rl")

        source = "TGJU"
        if price is None:
            logger.info("TGJU failed for USD/IRR. Using moneyconvert fallback...")
            price = TGJUService._fetch_exchangerate_to_irr("USD")
            source = "moneyconvert"

        if price is None:
            return None

        result = {
            "asset": "USD",
            "price": price,
            "currency": "IRR",
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
        }
        cache_service.set("usd_irr", result, Config.USD_IRR_CACHE_MINUTES)
        logger.info(f"USD/IRR fetched: {price} ({source})")
        return result

    @staticmethod
    def get_eur_to_irr() -> dict | None:
        cached = cache_service.get("eur_irr")
        if cached:
            return cached

        logger.info("Fetching EUR/IRR from TGJU...")
        price = TGJUService._fetch_tgju("price_eur")

        source = "TGJU"
        if price is None:
            logger.info("TGJU failed for EUR/IRR. Using moneyconvert fallback...")
            price = TGJUService._fetch_exchangerate_to_irr("EUR")
            source = "moneyconvert"

        if price is None:
            return None

        result = {
            "asset": "EUR",
            "price": price,
            "currency": "IRR",
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
        }
        cache_service.set("eur_irr", result, Config.EUR_IRR_CACHE_MINUTES)
        logger.info(f"EUR/IRR fetched: {price} ({source})")
        return result

    @staticmethod
    def get_gold_price() -> dict | None:
        cached = cache_service.get("gold_price")
        if cached:
            return cached

        price = None
        source = None

        logger.info("Fetching Gold price from TGJU...")
        price = TGJUService._fetch_tgju("sekee")
        if price is not None and price > 0:
            source = "TGJU"
        else:
            logger.info("TGJU failed for Gold price. Using market estimate...")
            # Fallback: use fixed gold price (~$2000/oz) and convert to IRR
            try:
                usd_irr_data = TGJUService.get_usd_to_irr()
                if usd_irr_data is not None:
                    usd_irr_rate = usd_irr_data["price"]
                    # Market estimate: ~$2000 per troy ounce, sekee is 1/4 oz
                    gold_price_usd_per_oz = 2000
                    price = (gold_price_usd_per_oz / 4) * usd_irr_rate
                    source = f"Market Estimate (~${gold_price_usd_per_oz}/oz)+TGJU(USD/IRR)"
                    logger.info(f"Gold price calculated using market estimate: {price:.0f} IRR")
                else:
                    logger.warning("Could not get USD/IRR rate for gold price estimate")
            except Exception as e:
                logger.error(f"Error calculating gold price estimate: {e}")

        if price is None or price <= 0:
            logger.error("Failed to fetch or estimate gold price from all sources")
            return None

        # Calculate price per gram (sekee is 1/4 troy ounce = 7.77588 grams)
        grams_per_sekee = 7.77588
        price_per_gram = price / grams_per_sekee

        result = {
            "asset": "Gold Coin (Sekee)",
            "price_coin": price,  # Price for 1/4 troy ounce (sekee)
            "price_per_gram": price_per_gram,  # Price per gram
            "weight_grams": grams_per_sekee,
            "currency": "IRR",
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
        }
        cache_service.set("gold_price", result, Config.GOLD_CACHE_MINUTES)
        logger.info(f"Gold price fetched: Coin={price:.0f} IRR, Per gram={price_per_gram:.0f} IRR ({source})")
        return result


class OilService:
    """Service for oil price data"""

    @staticmethod
    def _fetch_yahoo(symbol: str) -> float | None:
        try:
            r = requests.get(
                f"{YAHOO_API}/{symbol}",
                headers=HEADERS,
                timeout=Config.REQUEST_TIMEOUT,
            )
            r.raise_for_status()
            return r.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]
        except Exception as e:
            logger.error(f"Yahoo Finance fetch error ({symbol}): {e}")
            return None

    @staticmethod
    def get_wti_price() -> dict | None:
        cached = cache_service.get("wti_oil")
        if cached:
            return cached

        logger.info("Fetching WTI oil price...")
        price = OilService._fetch_yahoo("CL=F")
        if price is None:
            return None

        result = {
            "asset": "WTI Crude Oil",
            "symbol": "CL=F",
            "price_usd": price,
            "unit": "per barrel",
            "timestamp": datetime.utcnow().isoformat(),
            "source": "Yahoo Finance",
        }
        cache_service.set("wti_oil", result, Config.OIL_CACHE_MINUTES)
        logger.info(f"WTI price fetched: ${price}")
        return result

    @staticmethod
    def get_brent_price() -> dict | None:
        cached = cache_service.get("brent_oil")
        if cached:
            return cached

        logger.info("Fetching Brent oil price...")
        price = OilService._fetch_yahoo("BZ=F")
        if price is None:
            return None

        result = {
            "asset": "Brent Crude Oil",
            "symbol": "BZ=F",
            "price_usd": price,
            "unit": "per barrel",
            "timestamp": datetime.utcnow().isoformat(),
            "source": "Yahoo Finance",
        }
        cache_service.set("brent_oil", result, Config.OIL_CACHE_MINUTES)
        logger.info(f"Brent price fetched: ${price}")
        return result
