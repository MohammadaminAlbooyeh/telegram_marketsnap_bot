# Stock handlers - cryptocurrency and alert commands
from telegram import Update
from telegram.ext import ContextTypes
from services.stock_service import CryptoService, AlertService
from utils.validators import validate_price, validate_alert_condition
from utils.logger import logger

async def bitcoin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /bitcoin command"""

    data = CryptoService.get_bitcoin_price()

    if not data:
        await update.message.reply_text("❌ Failed to fetch Bitcoin price.")
        return

    message = (
        f"₿ Bitcoin (BTC)\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Price: ${data['price_usd']:,.2f}\n"
        f"IRR: {data['price_irr']:,.0f}\n\n"
        f"24h Change: {data['change_24h']:+.2f}% {'📈' if data['change_24h'] > 0 else '📉'}\n\n"
        f"Source: {data['source']}\n"
        f"Time: {data['timestamp']}"
    )

    logger.info(f"User {update.effective_user.id} requested Bitcoin price")
    await update.message.reply_text(message)

async def ethereum(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /ethereum command"""

    data = CryptoService.get_ethereum_price()

    if not data:
        await update.message.reply_text("❌ Failed to fetch Ethereum price.")
        return

    message = (
        f"Ξ Ethereum (ETH)\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Price: ${data['price_usd']:,.2f}\n"
        f"IRR: {data['price_irr']:,.0f}\n\n"
        f"24h Change: {data['change_24h']:+.2f}% {'📈' if data['change_24h'] > 0 else '📉'}\n\n"
        f"Source: {data['source']}\n"
        f"Time: {data['timestamp']}"
    )

    logger.info(f"User {update.effective_user.id} requested Ethereum price")
    await update.message.reply_text(message)

async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /crypto command - show top 10 cryptos"""

    cryptos = CryptoService.get_top_cryptos(limit=10)

    if not cryptos:
        await update.message.reply_text("❌ Failed to fetch cryptocurrency data.")
        return

    message = "📊 Top 10 Cryptocurrencies\n━━━━━━━━━━━━━━━━━━━\n\n"

    for crypto in cryptos:
        message += (
            f"{crypto['rank']}. {crypto['name']} ({crypto['symbol']})\n"
            f"   ${crypto['price_usd']:,.2f} | {crypto['price_irr']:,.0f} IRR\n"
            f"   24h: {crypto['change_24h']:+.2f}% {'📈' if crypto['change_24h'] > 0 else '📉'}\n\n"
        )

    await update.message.reply_text(message)

async def alerts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /alerts command - show user's alerts"""
    user_id = update.effective_user.id
    user_alerts = AlertService.get_user_alerts(user_id)

    if not user_alerts:
        await update.message.reply_text("📭 You have no active alerts.")
        return

    message = "🔔 Your Price Alerts\n━━━━━━━━━━━━━━━━━━━\n\n"
    for i, alert in enumerate(user_alerts, 1):
        message += (
            f"{i}. {alert['asset_name'].upper()}\n"
            f"   Condition: {alert['condition']} {alert['target_price']:,.0f} {alert['currency']}\n"
            f"   Created: {alert['created_at']}\n\n"
        )

    logger.info(f"User {user_id} viewed alerts")
    await update.message.reply_text(message)


async def setalert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /setalert command - create new alert"""
    if len(context.args) < 3:
        await update.message.reply_text(
            "Usage: /setalert <asset> <price> <above|below>\n"
            "Example: /setalert bitcoin 3000000 above"
        )
        return

    asset_name = context.args[0].lower()
    try:
        target_price = validate_price(context.args[1])
        condition = validate_alert_condition(context.args[2])
    except ValueError as e:
        await update.message.reply_text(f"❌ {e}")
        return

    user_id = update.effective_user.id
    success = AlertService.create_alert(
        user_id=user_id,
        asset_type="crypto",
        asset_name=asset_name,
        target_price=target_price,
        condition=condition
    )

    if success:
        await update.message.reply_text(
            f"✅ Alert created!\n"
            f"Asset: {asset_name.upper()}\n"
            f"Condition: {condition} {target_price:,.0f} IRR"
        )
        logger.info(f"User {user_id} created alert for {asset_name}")
    else:
        await update.message.reply_text("❌ Failed to create alert.")