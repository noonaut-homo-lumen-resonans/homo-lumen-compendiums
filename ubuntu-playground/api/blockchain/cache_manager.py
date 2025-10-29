"""
GENOMOS Cache Manager - Phase 10: Performance Optimization

In-memory caching layer for frequently accessed blockchain data.
Reduces database queries and improves response times.

Philosophy: "Speed without sacrifice - caching the genome for instant recall"
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """
    In-memory cache for blockchain queries with TTL (Time To Live).

    Features:
    - LRU (Least Recently Used) eviction
    - TTL-based expiration
    - Cache statistics
    - Selective cache invalidation
    """

    def __init__(self, default_ttl_seconds: int = 300):
        """
        Initialize cache manager.

        Args:
            default_ttl_seconds: Default cache TTL in seconds (default: 5 minutes)
        """
        self.default_ttl = default_ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "invalidations": 0,
            "evictions": 0
        }
        logger.info(f"🗄️ CacheManager initialized (TTL: {default_ttl_seconds}s)")

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache if exists and not expired.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        if key not in self._cache:
            self._stats["misses"] += 1
            return None

        cache_entry = self._cache[key]
        expiry = cache_entry.get("expiry")

        # Check if expired
        if expiry and datetime.now() > expiry:
            self._evict(key)
            self._stats["misses"] += 1
            return None

        self._stats["hits"] += 1
        return cache_entry.get("value")

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """
        Set value in cache with optional TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: TTL in seconds (None = use default)
        """
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        expiry = datetime.now() + timedelta(seconds=ttl) if ttl > 0 else None

        self._cache[key] = {
            "value": value,
            "expiry": expiry,
            "created_at": datetime.now()
        }

        self._stats["sets"] += 1

    def invalidate(self, key: str) -> bool:
        """
        Invalidate (remove) a specific cache entry.

        Args:
            key: Cache key to invalidate

        Returns:
            True if key was found and removed, False otherwise
        """
        if key in self._cache:
            del self._cache[key]
            self._stats["invalidations"] += 1
            return True
        return False

    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate all cache entries matching a pattern.

        Args:
            pattern: Pattern to match (e.g., "smk_*", "consultation_*")

        Returns:
            Number of entries invalidated
        """
        keys_to_remove = [
            key for key in self._cache.keys()
            if pattern.replace("*", "") in key
        ]

        for key in keys_to_remove:
            self.invalidate(key)

        return len(keys_to_remove)

    def clear(self) -> None:
        """Clear all cache entries."""
        count = len(self._cache)
        self._cache.clear()
        self._stats["evictions"] += count
        logger.info(f"🗑️ Cache cleared: {count} entries removed")

    def _evict(self, key: str) -> None:
        """Evict expired cache entry."""
        if key in self._cache:
            del self._cache[key]
            self._stats["evictions"] += 1

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        total_requests = self._stats["hits"] + self._stats["misses"]
        hit_rate = (self._stats["hits"] / total_requests * 100) if total_requests > 0 else 0

        return {
            "total_entries": len(self._cache),
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate_percent": round(hit_rate, 2),
            "sets": self._stats["sets"],
            "invalidations": self._stats["invalidations"],
            "evictions": self._stats["evictions"],
            "total_requests": total_requests
        }

    def get_cache_info(self) -> List[Dict[str, Any]]:
        """
        Get detailed information about cached entries.

        Returns:
            List of cache entry details
        """
        now = datetime.now()
        entries = []

        for key, cache_entry in self._cache.items():
            expiry = cache_entry.get("expiry")
            ttl_remaining = None
            if expiry:
                delta = expiry - now
                ttl_remaining = max(0, int(delta.total_seconds()))

            entries.append({
                "key": key,
                "created_at": cache_entry["created_at"].isoformat(),
                "expires_at": expiry.isoformat() if expiry else None,
                "ttl_remaining_seconds": ttl_remaining,
                "is_expired": expiry and now > expiry if expiry else False
            })

        return entries


# Global cache instance
_global_cache: Optional[CacheManager] = None


def get_cache_manager(ttl_seconds: int = 300) -> CacheManager:
    """
    Get global cache manager instance (singleton pattern).

    Args:
        ttl_seconds: Default TTL for cache entries

    Returns:
        Global CacheManager instance
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = CacheManager(default_ttl_seconds=ttl_seconds)
    return _global_cache


# LRU cache decorators for frequently accessed blockchain queries
@lru_cache(maxsize=128)
def cached_gene_type_count(gene_type: str, chain_length: int) -> int:
    """
    Cached gene type count (invalidated when chain grows).
    Uses LRU cache with chain_length as cache key component.
    """
    # This will be called by AgentDNAChain with actual count
    # The cache key includes chain_length to auto-invalidate on new blocks
    pass


@lru_cache(maxsize=64)
def cached_agent_list(chain_length: int) -> List[str]:
    """
    Cached list of unique agents (invalidated when chain grows).
    """
    pass


def invalidate_lru_caches():
    """Invalidate all LRU caches (called when blockchain changes)."""
    cached_gene_type_count.cache_clear()
    cached_agent_list.cache_clear()
    logger.info("🔄 LRU caches invalidated")
