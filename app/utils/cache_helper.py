from app.services.price_cache_service import cache_service


class CacheHelper:
    """Helper methods for cache operations."""

    @staticmethod
    def clear_all():
        cache_service.clear()

    @staticmethod
    def get_stats():
        return cache_service.get_stats()
