import functools
from app.core.logger import logger


def log_user_access(func):
    """Decorator to log user access."""
    @functools.wraps(func)
    async def wrapper(update, context):
        if update.effective_user:
            user_id = update.effective_user.id
            username = update.effective_user.username or "unknown"
            logger.info(f"User {user_id} (@{username}) accessed {func.__name__}")
        return await func(update, context)
    return wrapper
