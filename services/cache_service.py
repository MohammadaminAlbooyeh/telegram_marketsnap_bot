# Cache service - in-memory caching for fast price retrieval
from datetime import datetime, timedelta
from utils.logger import logger
import json

class CacheService:
    """In-memory cache service for price data"""
    
    def __init__(self):
        self.cache = {}  # {key: {value, expires_at}}
    
    def get(self, key: str):
        """Get cached value if not expired"""
        if key not in self.cache:
            return None
        
        cached_data = self.cache[key]
        
        # Check if expired
        if datetime.utcnow() > cached_data["expires_at"]:
            del self.cache[key]
            logger.info(f"Cache expired: {key}")
            return None
        
        logger.info(f"Cache hit: {key}")
        return cached_data["value"]
    
    def set(self, key: str, value, ttl_minutes: int):
        """Set cache value with TTL"""
        expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
        self.cache[key] = {
            "value": value,
            "expires_at": expires_at
        }
        logger.info(f"Cache set: {key} (expires in {ttl_minutes} minutes)")
    
    def delete(self, key: str):
        """Delete cache entry"""
        if key in self.cache:
            del self.cache[key]
            logger.info(f"Cache deleted: {key}")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_stats(self):
        """Get cache statistics"""
        return {
            "total_entries": len(self.cache),
            "keys": list(self.cache.keys())
        }

# Create global cache instance
cache_service = CacheService()