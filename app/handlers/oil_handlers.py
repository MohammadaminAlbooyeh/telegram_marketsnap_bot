# Oil handlers - oil price commands
from telegram import Update
from telegram.ext import ContextTypes
from app.services.oil_service import OilService
from app.core.logger import logger

async def oil(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /oil command - show both WTI and Brent prices"""
    
    wti_data = OilService.get_wti_price()
    brent_data = OilService.get_brent_price()
    
    if not wti_data or not brent_data:
        await update.message.reply_text("❌ Failed to fetch oil prices.")
        return
    
    message = (
        "🛢️ Oil Prices\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        f"WTI Crude Oil: ${wti_data['price_usd']:.2f} per barrel\n\n"
        f"Brent Crude Oil: ${brent_data['price_usd']:.2f} per barrel\n\n"
        f"Source: {wti_data['source']}\n"
        f"Time: {wti_data['timestamp']}"
    )
    
    logger.info(f"User {update.effective_user.id} requested oil prices")
    await update.message.reply_text(message)