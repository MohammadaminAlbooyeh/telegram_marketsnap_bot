from telegram import Update
from telegram.ext import ContextTypes
from app.services.tgju_service import TGJUService
from app.core.logger import logger


async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /gold command - show gold coin price"""
    data = TGJUService.get_gold_price()

    if not data:
        await update.message.reply_text("❌ Failed to fetch gold price.")
        return

    message = (
        f"🥇 Gold Coin Price\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Price: {data['price']:,.0f} IRR\n\n"
        f"Source: {data['source']}\n"
        f"Time: {data['timestamp']}"
    )

    logger.info(f"User {update.effective_user.id} requested gold price")
    await update.message.reply_text(message)
