"""
Performance Caching Module for MedhaOne Access Control

Provides global caching functionality to improve performance across
multiple sessions and requests.
"""

import time
from typing import Any, Dict, Optional, Set
from functools import wraps
from threading import RLock


class PerformanceCache:
    """
    High-performance LRU cache with TTL support for access control operations.
    
    This cache is designed to store:
    - Resolved expression results
    - User access resolutions
    - Frequently accessed database entities
    """
    
    def __init__(self, max_size: int = 10000, default_ttl: int = 300):
        """
        Initialize the performance cache.
        
        Args:
            max_size: Maximum number of items to cache
            default_ttl: Default time-to-live in seconds
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_times: Dict[str, float] = {}
        self._lock = RLock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get an item from the cache."""
        with self._lock:
            if key not in self._cache:
                return None
                
            item = self._cache[key]
            current_time = time.time()
            
            # Check if item has expired
            if current_time > item['expires_at']:
                self._remove(key)
                return None
            
            # Update access time for LRU
            self._access_times[key] = current_time
            return item['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set an item in the cache."""
        with self._lock:
            if ttl is None:
                ttl = self.default_ttl
                
            current_time = time.time()
            
            # If cache is full, remove LRU item
            if len(self._cache) >= self.max_size and key not in self._cache:
                self._evict_lru()
            
            # Store the item
            self._cache[key] = {
                'value': value,
                'created_at': current_time,
                'expires_at': current_time + ttl
            }
            self._access_times[key] = current_time
    
    def delete(self, key: str) -> bool:
        """Delete an item from the cache."""
        with self._lock:
            if key in self._cache:
                self._remove(key)
                return True
            return False
    
    def clear(self) -> None:
        """Clear all items from the cache."""
        with self._lock:
            self._cache.clear()
            self._access_times.clear()
    
    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate all cache keys matching a pattern.
        
        Args:
            pattern: String pattern to match against keys
            
        Returns:
            Number of items invalidated
        """
        with self._lock:
            keys_to_remove = [key for key in self._cache.keys() if pattern in key]
            for key in keys_to_remove:
                self._remove(key)
            return len(keys_to_remove)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            current_time = time.time()
            expired_count = sum(
                1 for item in self._cache.values() 
                if current_time > item['expires_at']
            )
            
            return {
                'size': len(self._cache),
                'max_size': self.max_size,
                'expired_items': expired_count,
                'hit_rate': getattr(self, '_hits', 0) / max(getattr(self, '_total_requests', 1), 1)
            }
    
    def _remove(self, key: str) -> None:
        """Remove an item from internal structures."""
        self._cache.pop(key, None)
        self._access_times.pop(key, None)
    
    def _evict_lru(self) -> None:
        """Evict the least recently used item."""
        if not self._access_times:
            return
            
        # Find the key with the oldest access time
        lru_key = min(self._access_times, key=self._access_times.get)
        self._remove(lru_key)


# Global cache instance
_global_cache = PerformanceCache(max_size=50000, default_ttl=600)  # 10 minute TTL


def cached_expression_resolution(cache_key_func):
    """
    Decorator for caching expression resolution results.
    
    Args:
        cache_key_func: Function that generates cache key from method arguments
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = cache_key_func(*args, **kwargs)
            
            # Try to get from cache first
            cached_result = _global_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            _global_cache.set(cache_key, result, ttl=300)  # 5 minute TTL for expressions
            
            return result
        return wrapper
    return decorator


def cache_user_access_resolution(user_id: str, app_name: Optional[str] = None, ttl: int = 60):
    """
    Cache user access resolution results.
    
    Args:
        user_id: User ID being resolved
        app_name: Application name filter
        ttl: Time to live in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"user_access:{user_id}:{app_name or 'all'}:{kwargs.get('evaluation_time', 'current')}"
            
            # Try to get from cache first
            cached_result = _global_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            _global_cache.set(cache_key, result, ttl=ttl)
            
            return result
        return wrapper
    return decorator


def invalidate_user_cache(user_id: str) -> int:
    """
    Invalidate all cached data for a specific user.
    
    Args:
        user_id: User ID to invalidate
        
    Returns:
        Number of cache entries invalidated
    """
    return _global_cache.invalidate_pattern(f"user:{user_id}") + \
           _global_cache.invalidate_pattern(f"user_access:{user_id}")


def invalidate_resource_cache(resource_id: str) -> int:
    """
    Invalidate all cached data for a specific resource.
    
    Args:
        resource_id: Resource ID to invalidate
        
    Returns:
        Number of cache entries invalidated
    """
    return _global_cache.invalidate_pattern(f"resource:{resource_id}")


def get_cache_stats() -> Dict[str, Any]:
    """Get global cache statistics."""
    return _global_cache.get_stats()


def clear_all_caches() -> None:
    """Clear all global caches."""
    _global_cache.clear()


# Export cache utilities
__all__ = [
    "PerformanceCache",
    "cached_expression_resolution", 
    "cache_user_access_resolution",
    "invalidate_user_cache",
    "invalidate_resource_cache",
    "get_cache_stats",
    "clear_all_caches",
]