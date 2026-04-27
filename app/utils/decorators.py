import functools
import time
import asyncio
from app.core.logger import logger


def log_execution_time(func):
    """Decorator to log execution time — supports both sync and async functions."""
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        logger.info(f"{func.__name__} executed in {time.time() - start:.4f}s")
        return result

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} executed in {time.time() - start:.4f}s")
        return result

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
