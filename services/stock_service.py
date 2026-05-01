# Stock service - cryptocurrency prices, alerts, and user management
import requests
from telegram import Bot
from config import Config
from utils.logger import logger
from utils.database import db
from services.cache_service import cache_service
from services.market_service import TGJUService
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


class AlertService:
    """Service for managing price alerts"""

    @staticmethod
    def create_alert(user_id: int, asset_type: str, asset_name: str,
                    target_price: float, condition: str, currency: str = "IRR") -> bool:
        """Create new price alert for user"""
        try:
            db.execute_update(
                """INSERT INTO user_alerts
                   (user_id, asset_type, asset_name, target_price, condition, currency)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, asset_type, asset_name, target_price, condition, currency)
            )
            logger.info(f"Alert created for user {user_id}: {asset_name} {condition} {target_price}")
            return True
        except Exception as e:
            logger.error(f"Error creating alert: {str(e)}")
            return False

    @staticmethod
    def get_user_alerts(user_id: int) -> list:
        """Get all active alerts for user"""
        results = db.execute_query(
            """SELECT * FROM user_alerts
               WHERE user_id = ? AND is_active = 1
               ORDER BY created_at DESC""",
            (user_id,)
        )
        return [dict(row) for row in results]

    @staticmethod
    def delete_alert(alert_id: int) -> bool:
        """Delete alert by ID"""
        try:
            db.execute_update(
                "UPDATE user_alerts SET is_active = 0 WHERE id = ?",
                (alert_id,)
            )
            logger.info(f"Alert deleted: {alert_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting alert: {str(e)}")
            return False

    @staticmethod
    def check_all_alerts(current_prices: dict) -> list:
        """Check all active alerts and trigger if condition met"""
        triggered_alerts = []

        try:
            # Get all active alerts
            results = db.execute_query(
                "SELECT * FROM user_alerts WHERE is_active = 1"
            )

            for row in results:
                alert = dict(row)
                asset_key = f"{alert['asset_type']}_{alert['asset_name']}"

                if asset_key in current_prices:
                    current_price = current_prices[asset_key]

                    # Check condition
                    if alert['condition'] == 'above' and current_price >= alert['target_price']:
                        triggered_alerts.append(alert)
                        AlertService._mark_triggered(alert['id'])

                    elif alert['condition'] == 'below' and current_price <= alert['target_price']:
                        triggered_alerts.append(alert)
                        AlertService._mark_triggered(alert['id'])

            if triggered_alerts:
                logger.info(f"{len(triggered_alerts)} alerts triggered")

            return triggered_alerts

        except Exception as e:
            logger.error(f"Error checking alerts: {str(e)}")
            return []

    @staticmethod
    def _mark_triggered(alert_id: int):
        """Mark alert as triggered"""
        db.execute_update(
            """UPDATE user_alerts
               SET triggered_at = ?, is_active = 0
               WHERE id = ?""",
            (datetime.utcnow().isoformat(), alert_id)
        )


class UserService:
    """Service for user-related operations"""

    @staticmethod
    def create_or_get_user(user_id: int, first_name: str,
                           last_name: str = None, username: str = None) -> dict:
        """Create new user or get existing user"""
        try:
            result = db.execute_query(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            )
            if result:
                logger.info(f"User {user_id} accessed")
                return dict(result[0])

            db.execute_update(
                "INSERT INTO users (user_id, first_name, last_name, username) VALUES (?, ?, ?, ?)",
                (user_id, first_name, last_name, username)
            )
            logger.info(f"New user created: {user_id}")
            return UserService.get_user(user_id)
        except Exception as e:
            logger.error(f"Error creating/getting user {user_id}: {e}")
            return None

    @staticmethod
    def get_user(user_id: int) -> dict:
        """Get user by user_id"""
        try:
            result = db.execute_query(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            )
            return dict(result[0]) if result else None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None

    @staticmethod
    def toggle_notifications(user_id: int, enabled: bool) -> bool:
        """Toggle user notifications"""
        try:
            db.execute_update(
                "UPDATE users SET notifications_enabled = ? WHERE user_id = ?",
                (1 if enabled else 0, user_id)
            )
            return True
        except Exception as e:
            logger.error(f"Error toggling notifications for {user_id}: {e}")
            return False

    @staticmethod
    def set_language(user_id: int, language: str) -> bool:
        """Set user language preference"""
        try:
            db.execute_update(
                "UPDATE users SET language = ? WHERE user_id = ?",
                (language, user_id)
            )
            return True
        except Exception as e:
            logger.error(f"Error setting language for {user_id}: {e}")
            return False


class NotificationService:
    """Service for sending notifications to users."""

    _bot: Bot = None

    @classmethod
    def get_bot(cls) -> Bot:
        if cls._bot is None:
            cls._bot = Bot(token=Config.BOT_TOKEN)
        return cls._bot

    @classmethod
    async def send_alert(cls, user_id: int, message: str) -> bool:
        """Send alert notification to user."""
        try:
            bot = cls.get_bot()
            await bot.send_message(chat_id=user_id, text=message)
            logger.info(f"Alert sent to user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending alert to {user_id}: {e}")
            return False

    @classmethod
    async def send_message(cls, user_id: int, message: str) -> bool:
        """Send general message to user."""
        try:
            bot = cls.get_bot()
            await bot.send_message(chat_id=user_id, text=message)
            return True
        except Exception as e:
            logger.error(f"Error sending message to {user_id}: {e}")
            return False
