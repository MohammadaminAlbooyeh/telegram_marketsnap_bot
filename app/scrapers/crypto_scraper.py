import requests
from app.core.config import Config
from app.core.logger import logger


class CryptoScraper:
    """Alternative crypto scraper using Binance public API."""

    @staticmethod
    def get_btc_usd() -> float:
        """Get BTC/USDT price from Binance."""
        try:
            response = requests.get(
                f"{Config.BINANCE_URL}/ticker/price",
                params={"symbol": "BTCUSDT"},
                timeout=Config.REQUEST_TIMEOUT
            )
            data = response.json()
            price = float(data.get("price", 0))
            logger.info(f"Binance BTC price: {price}")
            return price
        except Exception as e:
            logger.error(f"Binance BTC error: {e}")
            return 0

    @staticmethod
    def get_eth_usd() -> float:
        """Get ETH/USDT price from Binance."""
        try:
            response = requests.get(
                f"{Config.BINANCE_URL}/ticker/price",
                params={"symbol": "ETHUSDT"},
                timeout=Config.REQUEST_TIMEOUT
            )
            data = response.json()
            price = float(data.get("price", 0))
            logger.info(f"Binance ETH price: {price}")
            return price
        except Exception as e:
            logger.error(f"Binance ETH error: {e}")
            return 0
