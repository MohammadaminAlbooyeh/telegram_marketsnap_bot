# Market handlers - exchange rates, gold, and oil price commands
from telegram import Update
from telegram.ext import ContextTypes
from services.market_service import TGJUService, OilService
from utils.logger import logger

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