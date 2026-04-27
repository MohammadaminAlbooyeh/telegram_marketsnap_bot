# Crypto service - fetch cryptocurrency prices from CoinGecko and Binance
import requests
from app.core.config import Config
from app.core.logger import logger
from app.services.price_cache_service import cache_service
from app.services.tgju_service import TGJUService
from datetime import datetime


class CryptoService:
    """Service for cryptocurrency prices"""

    @staticmethod
    def _get_irr_rate() -> float:
        """Get current USD to IRR rate with fallback."""
        try:
            data = TGJUService.get_usd_to_irr()
            if data and data.get("price"):
                return data["price"]
        except Exception as e:
            logger.warning(f"Failed to get IRR rate, using fallback: {e}")
        return 50000  # fallback rate

    @staticmethod
    def get_bitcoin_price() -> dict:
        """Get Bitcoin price in USD, EUR, and IRR"""
        cached = cache_service.get("bitcoin")
        if cached:
            return cached

        try:
            logger.info("Fetching Bitcoin price from CoinGecko...")

            response = requests.get(
                f"{Config.COINGECKO_URL}/simple/price",
                params={
                    "ids": "bitcoin",
                    "vs_currencies": "usd,eur",
                    "include_24hr_change": True
                },
                timeout=Config.REQUEST_TIMEOUT
            )
            response.raise_for_status()  # Check HTTP status

            data = response.json()
            bitcoin = data.get("bitcoin", {})

            usd_price = bitcoin.get("usd", 0)
            irr_rate = CryptoService._get_irr_rate()
            irr_price = usd_price * irr_rate

            result = {
                "asset": "Bitcoin",
                "symbol": "BTC",
                "price_usd": usd_price,
                "price_eur": bitcoin.get("eur", 0),
                "price_irr": irr_price,
                "change_24h": bitcoin.get("usd_24h_change", 0),
                "timestamp": datetime.utcnow().isoformat(),
                "source": "CoinGecko"
            }

            cache_service.set("bitcoin", result, Config.CRYPTO_CACHE_MINUTES)
            logger.info(f"Bitcoin price fetched: ${usd_price}")
            return result

        except Exception as e:
            logger.error(f"Error fetching Bitcoin price: {str(e)}")
            return None

    @staticmethod
    def get_ethereum_price() -> dict:
        """Get Ethereum price in USD, EUR, and IRR"""
        cached = cache_service.get("ethereum")
        if cached:
            return cached

        try:
            logger.info("Fetching Ethereum price from CoinGecko...")

            response = requests.get(
                f"{Config.COINGECKO_URL}/simple/price",
                params={
                    "ids": "ethereum",
                    "vs_currencies": "usd,eur",
                    "include_24hr_change": True
                },
                timeout=Config.REQUEST_TIMEOUT
            )
            response.raise_for_status()  # Check HTTP status

            data = response.json()
            ethereum = data.get("ethereum", {})

            usd_price = ethereum.get("usd", 0)
            irr_rate = CryptoService._get_irr_rate()
            irr_price = usd_price * irr_rate

            result = {
                "asset": "Ethereum",
                "symbol": "ETH",
                "price_usd": usd_price,
                "price_eur": ethereum.get("eur", 0),
                "price_irr": irr_price,
                "change_24h": ethereum.get("usd_24h_change", 0),
                "timestamp": datetime.utcnow().isoformat(),
                "source": "CoinGecko"
            }

            cache_service.set("ethereum", result, Config.CRYPTO_CACHE_MINUTES)
            logger.info(f"Ethereum price fetched: ${usd_price}")
            return result

        except Exception as e:
            logger.error(f"Error fetching Ethereum price: {str(e)}")
            return None

    @staticmethod
    def get_top_cryptos(limit: int = 10) -> list:
        """Get top cryptocurrencies by market cap"""
        cached = cache_service.get(f"top_cryptos_{limit}")
        if cached:
            return cached

        try:
            logger.info(f"Fetching top {limit} cryptocurrencies...")

            response = requests.get(
                f"{Config.COINGECKO_URL}/coins/markets",
                params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": limit,
                    "page": 1
                },
                timeout=Config.REQUEST_TIMEOUT
            )

            cryptos = response.json()
            irr_rate = CryptoService._get_irr_rate()

            result = [
                {
                    "rank": i + 1,
                    "name": crypto["name"],
                    "symbol": crypto["symbol"].upper(),
                    "price_usd": crypto.get("current_price", 0),
                    "price_irr": crypto.get("current_price", 0) * irr_rate,
                    "market_cap": crypto.get("market_cap", 0),
                    "change_24h": crypto.get("price_change_percentage_24h", 0)
                }
                for i, crypto in enumerate(cryptos)
            ]

            cache_service.set(f"top_cryptos_{limit}", result, Config.CRYPTO_CACHE_MINUTES)
            logger.info(f"Top {limit} cryptos fetched")
            return result

        except Exception as e:
            logger.error(f"Error fetching top cryptos: {str(e)}")
            return []
