import sys

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

from app.core.config import Config
from app.core.logger import logger
from app.handlers.start_handler import start
from app.handlers.crypto_handlers import bitcoin, ethereum, crypto
from app.handlers.currency_handlers import rates, usd, eur
from app.handlers.gold_handlers import gold
from app.handlers.oil_handlers import oil
from app.handlers.alert_handlers import alerts, setalert
from app.handlers.callback_handlers import button_callback
from app.handlers.error_handler import error_handler
from app.scrapers.scheduler import PriceScheduler


def main():
    """Start the bot."""
    if not Config.BOT_TOKEN:
        logger.error("BOT_TOKEN not set. Please set it in .env file.")
        sys.exit(1)

    application = Application.builder().token(Config.BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("bitcoin", bitcoin))
    application.add_handler(CommandHandler("ethereum", ethereum))
    application.add_handler(CommandHandler("crypto", crypto))
    application.add_handler(CommandHandler("rates", rates))
    application.add_handler(CommandHandler("usd", usd))
    application.add_handler(CommandHandler("eur", eur))
    application.add_handler(CommandHandler("gold", gold))
    application.add_handler(CommandHandler("oil", oil))
    application.add_handler(CommandHandler("alerts", alerts))
    application.add_handler(CommandHandler("setalert", setalert))

    # Callback handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    # Error handler
    application.add_error_handler(error_handler)

    # Start background price scheduler
    scheduler = PriceScheduler()
    scheduler.start()
    logger.info("Background scheduler started")

    logger.info("Starting bot...")

    try:
        # Run the bot until Ctrl-C is pressed
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        scheduler.stop()
        logger.info("Bot stopped, scheduler shutdown")


if __name__ == "__main__":
    main()
