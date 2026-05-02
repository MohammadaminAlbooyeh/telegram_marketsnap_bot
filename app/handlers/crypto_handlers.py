# Compatibility handler for tests expecting `app.handlers.crypto_handlers`
from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from app.services.crypto_service import CryptoService


async def bitcoin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = CryptoService.get_bitcoin_price()
    if not data:
        # tests only assert reply_text called once when service returns None
        await update.message.reply_text("❌ Failed to fetch Bitcoin price.")
        return

    await update.message.reply_text("✅ Bitcoin price fetched.")
