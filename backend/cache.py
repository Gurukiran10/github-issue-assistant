"""
Caching layer for GitHub API and analysis results
Improves performance and reduces API calls
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class InMemoryCache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self):
        self.cache: Dict[str, tuple] = {}  # (value, expiry_time)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self.cache:
            value, expiry = self.cache[key]
            if datetime.now() < expiry:
                logger.debug(f"Cache hit for {key}")
                return value
            else:
                del self.cache[key]
                logger.debug(f"Cache expired for {key}")
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """Set value in cache with TTL"""
        expiry = datetime.now() + timedelta(seconds=ttl_seconds)
        self.cache[key] = (value, expiry)
        logger.debug(f"Cached {key} with TTL {ttl_seconds}s")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def generate_key(self, repo_url: str, issue_number: int) -> str:
        """Generate cache key for issue"""
        key_str = f"{repo_url}#{issue_number}"
        return hashlib.md5(key_str.encode()).hexdigest()


# Global cache instance
_cache = InMemoryCache()


def get_cache() -> InMemoryCache:
    """Get global cache instance"""
    return _cache
