from telegram import Bot
from app.core.config import Config
from app.core.logger import logger


class NotificationService:
    """Service for sending notifications to users."""

    _bot: Bot = None

    @classmethod
    def get_bot(cls) -> Bot:
        if cls._bot is None:
            cls._bot = Bot(token=Config.BOT_TOKEN)
        return cls._bot

    @classmethod
    async def send_alert(cls, user_id: int, message: str) -> bool:
        """Send alert notification to user."""
        try:
            await cls.get_bot().send_message(chat_id=user_id, text=message)
            logger.info(f"Alert sent to user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to send alert to {user_id}: {e}")
            return False
