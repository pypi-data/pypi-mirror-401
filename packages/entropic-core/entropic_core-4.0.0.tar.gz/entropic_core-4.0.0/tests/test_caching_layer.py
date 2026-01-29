import pytest
import time
from unittest.mock import patch, MagicMock
from entropic_core.optimization.caching_layer import (
    MemoryCache, CacheManager, CacheBackend, get_cache, configure_cache
)


class TestMemoryCache:
    """Test MemoryCache"""
    
    def test_memory_cache_init(self):
        """Test MemoryCache initialization"""
        cache = MemoryCache()
        assert len(cache._cache) == 0
    
    def test_set_and_get(self):
        """Test setting and getting values"""
        cache = MemoryCache()
        
        cache.set('key1', 'value1', ttl=3600)
        result = cache.get('key1')
        
        assert result == 'value1'
    
    def test_get_nonexistent(self):
        """Test getting nonexistent key"""
        cache = MemoryCache()
        result = cache.get('nonexistent')
        
        assert result is None
    
    def test_expiration(self):
        """Test key expiration"""
        cache = MemoryCache()
        
        cache.set('key1', 'value1', ttl=1)
        time.sleep(1.1)
        result = cache.get('key1')
        
        assert result is None
    
    def test_delete(self):
        """Test deleting key"""
        cache = MemoryCache()
        
        cache.set('key1', 'value1')
        cache.delete('key1')
        result = cache.get('key1')
        
        assert result is None
    
    def test_clear(self):
        """Test clearing cache"""
        cache = MemoryCache()
        
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        cache.clear()
        
        assert cache.get('key1') is None
        assert cache.get('key2') is None
    
    def test_cleanup_expired(self):
        """Test cleaning up expired entries"""
        cache = MemoryCache()
        
        cache.set('key1', 'value1', ttl=1)
        cache.set('key2', 'value2', ttl=3600)
        
        time.sleep(1.1)
        cache.cleanup_expired()
        
        assert cache.get('key1') is None
        assert cache.get('key2') == 'value2'


class TestCacheManager:
    """Test CacheManager"""
    
    def test_cache_manager_init(self):
        """Test CacheManager initialization"""
        manager = CacheManager(backend='memory')
        
        assert manager.backend_name == 'memory'
        assert manager.hit_count == 0
        assert manager.miss_count == 0
    
    def test_cached_decorator(self):
        """Test cached decorator"""
        manager = CacheManager(backend='memory')
        
        call_count = 0
        
        @manager.cached(ttl=3600)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        result1 = expensive_function(5)
        result2 = expensive_function(5)
        
        assert result1 == 10
        assert result2 == 10
        assert call_count == 1  # Called only once due to caching
    
    def test_cache_stats(self):
        """Test cache statistics"""
        manager = CacheManager(backend='memory')
        
        manager.set('key1', 'value1')
        manager.get('key1')  # Hit
        manager.get('nonexistent')  # Miss
        
        stats = manager.stats()
        
        assert 'hits' in stats
        assert 'misses' in stats
        assert stats['hits'] == 1
        assert stats['misses'] == 1
    
    def test_cache_clear(self):
        """Test clearing cache"""
        manager = CacheManager(backend='memory')
        
        manager.set('key1', 'value1')
        manager.get('key1')  # Hit
        manager.get('nonexistent')  # Miss - increments miss_count
        manager.clear()
        
        assert manager.get('key1') is None
        # So we expect hit_count to be reset but miss_count to remain from previous operation
        assert manager.hit_count == 0
        assert manager.miss_count == 1
    
    def test_get_cache_function(self):
        """Test get_cache function"""
        cache = get_cache()
        assert isinstance(cache, CacheManager)
    
    def test_configure_cache(self):
        """Test configure_cache function"""
        cache = configure_cache(backend='memory')
        assert isinstance(cache, CacheManager)


class TestRedisCacheFallback:
    """Test Redis cache fallback to memory"""
    
    def test_redis_unavailable_fallback(self):
        """Test fallback to memory when Redis unavailable"""
        pytest.importorskip("redis", minversion=None)
        
        with patch('redis.Redis') as mock_redis:
            mock_redis.side_effect = ImportError("redis not installed")
            
            manager = CacheManager(backend='redis')
            
            # Should have fallen back to memory
            assert manager.backend_name == 'memory'
            
            # Should still work
            manager.set('key', 'value')
            assert manager.get('key') == 'value'
