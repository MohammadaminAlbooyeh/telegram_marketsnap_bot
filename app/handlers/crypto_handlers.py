# Crypto handlers - cryptocurrency commands
from telegram import Update
from telegram.ext import ContextTypes
from app.services.crypto_service import CryptoService
from app.core.logger import logger

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