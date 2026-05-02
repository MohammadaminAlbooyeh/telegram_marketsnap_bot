# Compatibility handler for tests expecting `app.handlers.gold_handlers`
from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from services.market_service import TGJUService


async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = TGJUService.get_gold_price()
    if not data:
        await update.message.reply_text("❌ Failed to fetch gold price.")
        return

    await update.message.reply_text("✅ Gold price fetched.")
