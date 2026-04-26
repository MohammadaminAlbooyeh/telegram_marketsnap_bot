import functools
from app.core.logger import logger


def log_execution_time(func):
    """Decorator to log execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} executed in {elapsed:.4f}s")
        return result
    return wrapper
