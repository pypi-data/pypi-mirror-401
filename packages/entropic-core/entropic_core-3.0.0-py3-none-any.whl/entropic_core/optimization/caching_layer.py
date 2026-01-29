"""Caching layer for performance optimization."""

import hashlib
import logging
import pickle
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class CacheBackend(ABC):
    """Abstract cache backend."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL."""

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete value from cache."""

    @abstractmethod
    def clear(self) -> bool:
        """Clear all cache."""


class MemoryCache(CacheBackend):
    """In-memory cache implementation."""

    def __init__(self):
        self._cache: Dict[str, tuple] = {}  # {key: (value, expiry_time)}
        logger.info("Initialized MemoryCache")

    def get(self, key: str) -> Optional[Any]:
        """Get value from memory cache."""
        if key in self._cache:
            value, expiry = self._cache[key]
            if expiry > time.time():
                logger.debug(f"Cache HIT: {key}")
                return value
            else:
                # Expired
                del self._cache[key]
                logger.debug(f"Cache EXPIRED: {key}")

        logger.debug(f"Cache MISS: {key}")
        return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in memory cache."""
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)
        logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
        return True

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache DELETE: {key}")
            return True
        return False

    def clear(self) -> bool:
        """Clear all cache."""
        self._cache.clear()
        logger.info("Cache cleared")
        return True

    def cleanup_expired(self):
        """Remove expired entries."""
        now = time.time()
        expired = [k for k, (_, expiry) in self._cache.items() if expiry <= now]
        for key in expired:
            del self._cache[key]
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired cache entries")


class RedisCache(CacheBackend):
    """Redis cache implementation."""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        try:
            import redis

            self.redis = redis.Redis(
                host=host, port=port, db=db, decode_responses=False
            )
            self.redis.ping()
            logger.info(f"Connected to Redis at {host}:{port}")
        except ImportError:
            logger.warning("Redis not installed, falling back to MemoryCache")
            raise ImportError("redis package not installed")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache."""
        try:
            value = self.redis.get(key)
            if value:
                logger.debug(f"Redis HIT: {key}")
                return pickle.loads(value)
            logger.debug(f"Redis MISS: {key}")
            return None
        except Exception as e:
            logger.error(f"Redis GET error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in Redis cache."""
        try:
            serialized = pickle.dumps(value)
            self.redis.setex(key, ttl, serialized)
            logger.debug(f"Redis SET: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Redis SET error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete value from Redis cache."""
        try:
            result = self.redis.delete(key)
            logger.debug(f"Redis DELETE: {key}")
            return result > 0
        except Exception as e:
            logger.error(f"Redis DELETE error: {e}")
            return False

    def clear(self) -> bool:
        """Clear all cache."""
        try:
            self.redis.flushdb()
            logger.info("Redis cache cleared")
            return True
        except Exception as e:
            logger.error(f"Redis CLEAR error: {e}")
            return False


class CacheManager:
    """High-level cache manager with fallback."""

    def __init__(self, backend: str = "memory", **kwargs):
        self.backend_name = backend

        if backend == "redis":
            try:
                self.backend = RedisCache(**kwargs)
            except (ImportError, Exception) as e:
                logger.warning(f"Redis unavailable, using MemoryCache: {e}")
                self.backend = MemoryCache()
                self.backend_name = "memory"
        else:
            self.backend = MemoryCache()

        self.hit_count = 0
        self.miss_count = 0

    def _make_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get from cache."""
        value = self.backend.get(key)
        if value is not None:
            self.hit_count += 1
        else:
            self.miss_count += 1
        return value

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set in cache."""
        return self.backend.set(key, value, ttl)

    def cached(self, ttl: int = 3600):
        """Decorator for caching function results."""

        def decorator(func):
            def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}:{self._make_key(*args, **kwargs)}"

                # Try cache first
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return cached_value

                # Compute and cache
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result

            return wrapper

        return decorator

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total * 100) if total > 0 else 0

        return {
            "backend": self.backend_name,
            "hits": self.hit_count,
            "misses": self.miss_count,
            "total_requests": total,
            "hit_rate": round(hit_rate, 2),
        }

    def clear(self) -> bool:
        """Clear cache and stats."""
        self.hit_count = 0
        self.miss_count = 0
        return self.backend.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics (alias for stats method)"""
        return self.stats()


# Global cache instance
_cache = CacheManager()


def get_cache() -> CacheManager:
    """Get global cache instance."""
    return _cache


def configure_cache(backend: str = "memory", **kwargs):
    """Configure global cache."""
    global _cache
    _cache = CacheManager(backend=backend, **kwargs)
    return _cache
