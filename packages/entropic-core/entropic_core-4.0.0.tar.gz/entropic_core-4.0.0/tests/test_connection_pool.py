import pytest
import time
import threading
from entropic_core.optimization.connection_pool import Connection, ConnectionPool


class TestConnectionPool:
    """Test ConnectionPool functionality"""
    
    def create_mock_connection(self):
        """Create a mock connection factory"""
        class MockConnection:
            def __init__(self):
                self.closed = False
            def close(self):
                self.closed = True
        return MockConnection()
    
    def test_connection_pool_init(self):
        """Test ConnectionPool initialization"""
        pool = ConnectionPool(self.create_mock_connection, min_size=2, max_size=5)
        
        assert pool.min_size == 2
        assert pool.max_size == 5
        assert pool.size >= 2
    
    def test_acquire_release_connection(self):
        """Test acquiring and releasing connections"""
        pool = ConnectionPool(self.create_mock_connection, min_size=1, max_size=3)
        
        conn = pool.acquire(timeout=1)
        assert conn is not None
        
        pool.release(conn)
        # Connection should be back in pool
    
    
    def test_connection_expiry_by_lifetime(self):
        """Test connection expiry by max lifetime"""
        pool = ConnectionPool(
            self.create_mock_connection,
            min_size=1,
            max_size=5,
            max_lifetime=0.1  # 100ms
        )
        
        conn = pool.acquire()
        time.sleep(0.15)
        
        # Connection should be expired
        assert pool._is_expired(conn)
    
    def test_connection_expiry_by_idle_time(self):
        """Test connection expiry by idle time"""
        pool = ConnectionPool(
            self.create_mock_connection,
            min_size=1,
            max_size=5,
            max_idle_time=0.1  # 100ms
        )
        
        conn = pool.acquire()
        time.sleep(0.15)
        
        # Connection should be expired due to idle time
        assert pool._is_expired(conn)
    
    def test_pool_stats(self):
        """Test pool statistics"""
        pool = ConnectionPool(self.create_mock_connection, min_size=2, max_size=5)
        
        stats = pool.stats()
        assert 'pool_size' in stats
        assert 'available' in stats
        assert 'in_use' in stats
        assert 'created_total' in stats
        assert 'recycled_total' in stats
    
    def test_close_all_connections(self):
        """Test closing all connections"""
        pool = ConnectionPool(self.create_mock_connection, min_size=2, max_size=5)
        
        conn1 = pool.acquire()
        conn2 = pool.acquire()
        
        pool.release(conn1)
        pool.release(conn2)
        
        pool.close_all()
        # Pool should be closed
    
    def test_concurrent_acquisition(self):
        """Test concurrent connection acquisition"""
        pool = ConnectionPool(self.create_mock_connection, min_size=1, max_size=10)
        
        acquired = []
        
        def acquire_and_release():
            conn = pool.acquire()
            acquired.append(conn)
            time.sleep(0.01)
            pool.release(conn)
        
        threads = [threading.Thread(target=acquire_and_release) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        assert len(acquired) == 5


class TestConnection:
    """Test Connection wrapper"""
    
    def test_connection_context_manager(self):
        """Test Connection context manager"""
        class MockConn:
            pass
        
        class MockPool:
            def release(self, conn):
                pass
        
        mock_pool = MockPool()
        conn_wrapper = Connection(MockConn(), mock_pool)
        
        with conn_wrapper as conn:
            assert conn is not None
        
        assert conn_wrapper.use_count == 1
