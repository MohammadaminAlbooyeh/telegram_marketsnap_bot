# Compatibility handler for tests expecting `app.handlers.currency_handlers`
from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from services.market_service import TGJUService


async def usd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = TGJUService.get_usd_to_irr()
    if not data:
        await update.message.reply_text("❌ Failed to fetch USD rate.")
        return

    await update.message.reply_text("✅ USD rate fetched.")
