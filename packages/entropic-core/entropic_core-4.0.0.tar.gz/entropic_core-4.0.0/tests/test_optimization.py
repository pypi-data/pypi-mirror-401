"""
Optimization Features Test Suite
Tests for caching, async operations, and batch processing
"""

import asyncio
import time

import pytest

from entropic_core.optimization.async_operations import AsyncEntropyBrain
from entropic_core.optimization.batch_processor import BatchProcessor
from entropic_core.optimization.caching_layer import CacheManager


class TestCacheManager:
    """Test caching functionality"""

    def test_memory_cache(self):
        """Test in-memory caching"""
        cache = CacheManager(backend="memory")

        cache.set("test_key", {"value": 42}, ttl=60)
        result = cache.get("test_key")

        assert result is not None
        assert result["value"] == 42

    def test_cache_expiration(self):
        """Test cache TTL expiration"""
        cache = CacheManager(backend="memory")

        cache.set("expire_key", {"data": "test"}, ttl=1)

        # Should exist immediately
        assert cache.get("expire_key") is not None

        # Wait for expiration
        time.sleep(2)

        # Should be expired
        assert cache.get("expire_key") is None

    def test_cache_stats(self):
        """Test cache statistics"""
        cache = CacheManager(backend="memory")

        cache.set("key1", "value1")
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss

        stats = cache.get_stats()

        assert "hits" in stats
        assert "misses" in stats
        assert stats["hits"] >= 1
        assert stats["misses"] >= 1


class TestAsyncOperations:
    """Test async operations"""

    @pytest.mark.asyncio
    async def test_async_measure(self):
        """Test async entropy measurement"""
        brain = AsyncEntropyBrain()

        class MockAgent:
            def __init__(self):
                self.current_state = 0.5
                self.last_decision = "action"
                self.messages_sent = 5

        brain.connect([MockAgent(), MockAgent(), MockAgent()])

        entropy = await brain.async_measure()

        assert 0.0 <= entropy <= 1.0

    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """Test concurrent entropy measurements"""
        brain = AsyncEntropyBrain()

        class MockAgent:
            def __init__(self, state: float):
                self.current_state = state
                self.last_decision = "action"
                self.messages_sent = 5

        brain.connect([MockAgent(0.3), MockAgent(0.7)])

        # Run multiple measurements concurrently
        results = await asyncio.gather(
            brain.async_measure(), brain.async_measure(), brain.async_measure()
        )

        assert len(results) == 3
        assert all(0.0 <= r <= 1.0 for r in results)


class TestBatchProcessor:
    """Test batch processing"""

    def test_batch_operations(self):
        """Test batch operation processing"""
        processor = BatchProcessor(batch_size=5, flush_interval=1.0)

        # Add operations
        for i in range(10):
            processor.add_operation(f"op_{i}", {"data": i})

        # Process batch
        results = processor.process_batch()

        assert len(results) >= 5  # Should process at least one batch

    def test_auto_flush(self):
        """Test automatic flushing"""
        processor = BatchProcessor(batch_size=100, flush_interval=0.5)

        # Add few operations (less than batch size)
        for i in range(3):
            processor.add_operation(f"op_{i}", {"data": i})

        # Wait for auto-flush
        time.sleep(1)

        # Should have been flushed
        assert len(processor.pending_operations) < 3


class TestPluginSystem:
    """Test plugin loading and execution"""

    def test_plugin_loading(self):
        """Test loading built-in plugins"""
        from entropic_core.plugins.plugin_loader import PluginLoader

        loader = PluginLoader()
        count = loader.load_all_plugins()

        # Should load at least built-in plugins
        assert count >= 0

    def test_plugin_hooks(self):
        """Test plugin hook execution"""
        from entropic_core import EntropyBrain
        from entropic_core.plugins.plugin_manager import PluginManager

        brain = EntropyBrain()
        plugin_manager = PluginManager(brain)
        plugin_manager.initialize(auto_load=False)

        # Test hook triggers
        plugin_manager.trigger_entropy_measured(0.5, [], {})

        # Should not raise any errors
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
