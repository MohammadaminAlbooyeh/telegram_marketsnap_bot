from apscheduler.schedulers.background import BackgroundScheduler
from app.core.logger import logger
from app.services.tgju_service import TGJUService
from app.services.crypto_service import CryptoService
from app.services.oil_service import OilService
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
        self.scheduler.start()
        logger.info("Price scheduler started")

    def stop(self):
        """Stop scheduler."""
        self.scheduler.shutdown()
        logger.info("Price scheduler stopped")
