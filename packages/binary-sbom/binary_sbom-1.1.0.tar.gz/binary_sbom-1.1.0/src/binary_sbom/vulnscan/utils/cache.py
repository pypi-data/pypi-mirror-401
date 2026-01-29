"""
Caching layer for vulnerability query results.

This module provides caching to reduce API calls and improve performance.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from threading import Lock
from typing import Any

logger = logging.getLogger(__name__)


class VulnerabilityCache:
    """
    In-memory cache for vulnerability query results.

    Caches API responses to reduce redundant calls and improve performance.
    Implements time-based expiration (TTL) and LRU eviction when capacity is reached.

    Attributes:
        ttl: Cache time-to-live in seconds
        max_size: Maximum number of cached entries
        cache: Internal cache storage
        lock: Thread safety lock

    Example:
        >>> cache = VulnerabilityCache(ttl=3600)  # 1 hour TTL
        >>> key = cache.make_key("npm", "lodash", "4.17.15")
        >>> cache.put(key, {"vulnerabilities": [...]})
        >>> data = cache.get(key)
        >>> assert data["vulnerabilities"] is not None
    """

    def __init__(self, ttl: int = 3600, max_size: int = 1000):
        """
        Initialize vulnerability cache.

        Args:
            ttl: Cache time-to-live in seconds (default: 1 hour)
            max_size: Maximum number of cached entries

        Example:
            >>> cache = VulnerabilityCache(ttl=7200, max_size=2000)
            >>> cache.ttl
            7200
            >>> cache.max_size
            2000
        """
        self.ttl = ttl
        self.max_size = max_size
        self.cache: dict[str, dict[str, Any]] = {}
        self.lock = Lock()

    def get(self, key: str) -> dict[str, Any] | None:
        """
        Get cached value by key.

        Returns the cached value if it exists and has not expired.
        Returns None if the key does not exist or the entry has expired.

        Args:
            key: Cache key

        Returns:
            Cached value if exists and not expired, None otherwise

        Example:
            >>> cache = VulnerabilityCache(ttl=60)
            >>> key = cache.make_key("npm", "lodash", "4.17.15")
            >>> cache.put(key, {"data": "test"})
            >>> result = cache.get(key)
            >>> assert result["data"] == "test"
        """
        with self.lock:
            entry = self.cache.get(key)

            if entry is None:
                logger.debug(f"Cache miss for key: {key[:16]}...")
                return None

            # Check if entry has expired
            if time.time() > entry["expires_at"]:
                logger.debug(f"Cache entry expired for key: {key[:16]}...")
                del self.cache[key]
                return None

            # Update access time for LRU tracking
            entry["last_accessed"] = time.time()
            logger.debug(f"Cache hit for key: {key[:16]}...")
            return entry["value"]

    def put(self, key: str, value: dict[str, Any]) -> None:
        """
        Put value in cache.

        If the cache is at maximum capacity, evicts the least recently used entry
        before adding the new entry.

        Args:
            key: Cache key
            value: Value to cache

        Example:
            >>> cache = VulnerabilityCache(ttl=60, max_size=2)
            >>> key1 = cache.make_key("npm", "package1", "1.0.0")
            >>> key2 = cache.make_key("npm", "package2", "1.0.0")
            >>> key3 = cache.make_key("npm", "package3", "1.0.0")
            >>> cache.put(key1, {"data": "1"})
            >>> cache.put(key2, {"data": "2"})
            >>> cache.put(key3, {"data": "3"})  # Evicts key1 (LRU)
        """
        with self.lock:
            # Evict LRU entry if at capacity
            if len(self.cache) >= self.max_size and key not in self.cache:
                self._evict_lru()

            # Store cache entry with metadata
            self.cache[key] = {
                "value": value,
                "created_at": time.time(),
                "expires_at": time.time() + self.ttl,
                "last_accessed": time.time(),
            }
            logger.debug(f"Cached value for key: {key[:16]}... (expires in {self.ttl}s)")

    def make_key(self, *args: Any) -> str:
        """
        Create cache key from arguments.

        Creates a deterministic key by hashing the JSON representation
        of the arguments. This ensures identical queries generate the
        same cache key.

        Args:
            *args: Arguments to include in key

        Returns:
            SHA256 hash of arguments (hexadecimal string)

        Example:
            >>> cache = VulnerabilityCache()
            >>> key1 = cache.make_key("npm", "lodash", "4.17.15")
            >>> key2 = cache.make_key("npm", "lodash", "4.17.15")
            >>> key3 = cache.make_key("npm", "lodash", "4.17.16")
            >>> assert key1 == key2
            >>> assert key1 != key3
        """
        key_string = json.dumps(args, sort_keys=True)
        return hashlib.sha256(key_string.encode()).hexdigest()

    def clear(self) -> None:
        """
        Clear all cached entries.

        Removes all entries from the cache, resetting it to empty state.

        Example:
            >>> cache = VulnerabilityCache()
            >>> cache.put(cache.make_key("npm", "test", "1.0.0"), {"data": "test"})
            >>> assert len(cache.cache) > 0
            >>> cache.clear()
            >>> assert len(cache.cache) == 0
        """
        with self.lock:
            size = len(self.cache)
            self.cache.clear()
            logger.debug(f"Cleared {size} cached entries")

    def cleanup_expired(self) -> int:
        """
        Remove expired entries from cache.

        Iterates through all cache entries and removes those that have
        exceeded their time-to-live (TTL).

        Returns:
            Number of entries removed

        Example:
            >>> cache = VulnerabilityCache(ttl=0)  # Immediate expiry
            >>> key = cache.make_key("npm", "test", "1.0.0")
            >>> cache.put(key, {"data": "test"})
            >>> import time
            >>> time.sleep(0.1)  # Ensure expiry
            >>> removed = cache.cleanup_expired()
            >>> assert removed == 1
        """
        with self.lock:
            current_time = time.time()
            expired_keys = [
                key
                for key, entry in self.cache.items()
                if current_time > entry["expires_at"]
            ]

            for key in expired_keys:
                del self.cache[key]

            if expired_keys:
                logger.debug(f"Cleaned up {len(expired_keys)} expired entries")

            return len(expired_keys)

    def get_stats(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics including size, ttl, max_size,
            and number of expired entries

        Example:
            >>> cache = VulnerabilityCache(ttl=60, max_size=100)
            >>> stats = cache.get_stats()
            >>> assert stats["size"] == 0
            >>> assert stats["max_size"] == 100
        """
        with self.lock:
            current_time = time.time()
            expired_count = sum(
                1 for entry in self.cache.values() if current_time > entry["expires_at"]
            )

            return {
                "size": len(self.cache),
                "ttl": self.ttl,
                "max_size": self.max_size,
                "expired_count": expired_count,
            }

    def _evict_lru(self) -> None:
        """
        Evict the least recently used entry from the cache.

        Identifies the entry with the oldest last_accessed timestamp
        and removes it from the cache. This method should only be called
        when the cache is at maximum capacity.

        Example:
            >>> cache = VulnerabilityCache(max_size=2)
            >>> key1 = cache.make_key("a")
            >>> key2 = cache.make_key("b")
            >>> cache.put(key1, {"data": "1"})
            >>> cache.put(key2, {"data": "2"})
            >>> # Access key1 to make it more recent
            >>> cache.get(key1)
            >>> key3 = cache.make_key("c")
            >>> cache.put(key3, {"data": "3"})  # Evicts key2
            >>> assert cache.get(key2) is None
        """
        if not self.cache:
            return

        # Find entry with oldest last_accessed time
        lru_key = min(self.cache.keys(), key=lambda k: self.cache[k]["last_accessed"])
        logger.debug(f"Evicting LRU entry: {lru_key[:16]}...")
        del self.cache[lru_key]
