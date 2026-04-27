from apscheduler.schedulers.background import BackgroundScheduler
from app.core.logger import logger
from app.services.tgju_service import TGJUService
from app.services.crypto_service import CryptoService
from app.services.oil_service import OilService
from app.services.alert_service import AlertService
from app.core.config import Config


class PriceScheduler:
    """Background scheduler to keep cache warm."""

    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self):
        """Start background jobs."""
        self.scheduler.add_job(
            TGJUService.get_usd_to_irr,
            "interval",
            minutes=Config.TGJU_UPDATE_MINUTES,
            id="usd_irr_update"
        )
        self.scheduler.add_job(
            CryptoService.get_bitcoin_price,
            "interval",
            minutes=Config.CRYPTO_UPDATE_MINUTES,
            id="bitcoin_update"
        )
        self.scheduler.add_job(
            OilService.get_wti_price,
            "interval",
            minutes=Config.OIL_UPDATE_MINUTES,
            id="wti_update"
        )
        self.scheduler.add_job(
            self._check_alerts,
            "interval",
            minutes=Config.ALERT_CHECK_MINUTES,
            id="alert_check"
        )
        self.scheduler.start()
        logger.info("Price scheduler started")

    @staticmethod
    def _check_alerts():
        """Check all active alerts and trigger if conditions met."""
        try:
            # Collect current prices
            current_prices = {}
            
            usd_data = TGJUService.get_usd_to_irr()
            if usd_data:
                current_prices["currency_usd"] = usd_data.get("price", 0)
            
            btc_data = CryptoService.get_bitcoin_price()
            if btc_data:
                current_prices["crypto_bitcoin"] = btc_data.get("price_irr", 0)
            
            eth_data = CryptoService.get_ethereum_price()
            if eth_data:
                current_prices["crypto_ethereum"] = eth_data.get("price_irr", 0)
            
            wti_data = OilService.get_wti_price()
            if wti_data:
                current_prices["oil_wti"] = wti_data.get("price_usd", 0)
            
            # Check alerts with current prices
            AlertService.check_all_alerts(current_prices)
            logger.info("Alert check completed")
        except Exception as e:
            logger.error(f"Error in alert check job: {e}")

    def stop(self):
        """Stop scheduler."""
        self.scheduler.shutdown()
        logger.info("Price scheduler stopped")
