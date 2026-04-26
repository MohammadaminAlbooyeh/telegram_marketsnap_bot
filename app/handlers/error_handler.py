from telegram import Update
from telegram.ext import ContextTypes
from app.core.logger import logger


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and notify user."""
    logger.error(f"Exception while handling an update: {context.error}")

    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred while processing your request. Please try again later."
        )
