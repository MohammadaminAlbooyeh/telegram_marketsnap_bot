# Currency handlers - exchange rate commands
from telegram import Update
from telegram.ext import ContextTypes
from app.services.tgju_service import TGJUService
from app.core.logger import logger

async def rates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /rates command - show all exchange rates"""
    
    usd_data = TGJUService.get_usd_to_irr()
    eur_data = TGJUService.get_eur_to_irr()
    
    if not usd_data or not eur_data:
        await update.message.reply_text("❌ Failed to fetch exchange rates. Try again later.")
        return
    
    message = (
        "💱 Current Exchange Rates\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🇺🇸 USD → IRR\n"
        f"1 USD = {usd_data['price']:,.0f} IRR\n\n"
        f"🇪🇺 EUR → IRR\n"
        f"1 EUR = {eur_data['price']:,.0f} IRR\n\n"
        f"⏰ Updated: {usd_data['timestamp']}"
    )
    
    logger.info(f"User {update.effective_user.id} requested exchange rates")
    await update.message.reply_text(message)

async def usd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /usd command - USD to IRR rate"""
    
    data = TGJUService.get_usd_to_irr()
    
    if not data:
        await update.message.reply_text("❌ Failed to fetch USD rate.")
        return
    
    message = (
        f"🇺🇸 USD Exchange Rate\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"1 USD = {data['price']:,.0f} IRR\n\n"
        f"Source: {data['source']}\n"
        f"Time: {data['timestamp']}"
    )
    
    await update.message.reply_text(message)

async def eur(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /eur command - EUR to IRR rate"""
    
    data = TGJUService.get_eur_to_irr()
    
    if not data:
        await update.message.reply_text("❌ Failed to fetch EUR rate.")
        return
    
    message = (
        f"🇪🇺 EUR Exchange Rate\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"1 EUR = {data['price']:,.0f} IRR\n\n"
        f"Source: {data['source']}\n"
        f"Time: {data['timestamp']}"
    )
    
    await update.message.reply_text(message)