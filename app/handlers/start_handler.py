# Start handler - welcome message and main menu
from telegram import Update
from telegram.ext import ContextTypes
from app.services.user_service import UserService
from app.utils.keyboards import main_menu_keyboard
from app.core.logger import logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user

    UserService.create_or_get_user(
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username
    )

    logger.info(f"User {user.id} started bot")

    welcome_message = (
        f"👋 Welcome {user.first_name}!\n\n"
        "📊 MarketSnap Bot - Real-time Price Tracker\n\n"
        "Get instant updates on:\n"
        "• 💱 Exchange Rates (USD, EUR to IRR)\n"
        "• 🥇 Gold & Coin Prices\n"
        "• ₿ Cryptocurrency Prices\n"
        "• 🛢️ Oil Prices (WTI, Brent)\n"
        "• 🔔 Price Alerts\n\n"
        "Choose an option below:"
    )

    await update.message.reply_text(welcome_message, reply_markup=main_menu_keyboard())