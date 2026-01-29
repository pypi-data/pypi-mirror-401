"""Connection pooling for database and external services."""

import logging
import threading
import time
from queue import Empty, Queue
from typing import Any, Callable

logger = logging.getLogger(__name__)


class Connection:
    """Wrapper for a pooled connection."""

    def __init__(self, connection: Any, pool: "ConnectionPool"):
        self.connection = connection
        self.pool = pool
        self.created_at = time.time()
        self.last_used = time.time()
        self.use_count = 0

    def __enter__(self):
        """Context manager entry."""
        self.last_used = time.time()
        self.use_count += 1
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - return connection to pool."""
        self.pool.release(self)


class ConnectionPool:
    """Generic connection pool for any resource."""

    def __init__(
        self,
        factory: Callable,
        min_size: int = 2,
        max_size: int = 10,
        max_idle_time: float = 300.0,  # 5 minutes
        max_lifetime: float = 3600.0,  # 1 hour
    ):
        self.factory = factory
        self.min_size = min_size
        self.max_size = max_size
        self.max_idle_time = max_idle_time
        self.max_lifetime = max_lifetime

        self.pool = Queue(maxsize=max_size)
        self.size = 0
        self.lock = threading.Lock()

        # Statistics
        self.created_count = 0
        self.recycled_count = 0
        self.max_wait_time = 0.0

        # Initialize minimum connections
        self._initialize_pool()

        # Start cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()

        logger.info(f"Connection pool initialized (min: {min_size}, max: {max_size})")

    def _initialize_pool(self):
        """Create minimum number of connections."""
        for _ in range(self.min_size):
            self._create_connection()

    def _create_connection(self) -> Connection:
        """Create a new connection."""
        with self.lock:
            if self.size >= self.max_size:
                raise Exception("Connection pool exhausted")

            raw_conn = self.factory()
            conn = Connection(raw_conn, self)
            self.size += 1
            self.created_count += 1

            logger.debug(f"Created new connection (pool size: {self.size})")
            return conn

    def acquire(self, timeout: float = 10.0) -> Connection:
        """Acquire connection from pool."""
        start_time = time.time()

        try:
            # Try to get from pool
            conn = self.pool.get(timeout=timeout)

            # Check if connection is still valid
            if self._is_expired(conn):
                logger.debug("Connection expired, creating new one")
                self._close_connection(conn)
                conn = self._create_connection()

            wait_time = time.time() - start_time
            self.max_wait_time = max(self.max_wait_time, wait_time)

            return conn

        except Empty:
            # Pool empty, try to create new connection
            try:
                conn = self._create_connection()
                return conn
            except Exception as e:
                logger.error(f"Failed to acquire connection: {e}")
                raise

    def release(self, conn: Connection):
        """Release connection back to pool."""
        try:
            if self._is_expired(conn):
                self._close_connection(conn)
                # Create replacement if below minimum
                if self.size < self.min_size:
                    self._create_connection()
            else:
                self.pool.put_nowait(conn)
                self.recycled_count += 1

        except Exception as e:
            logger.error(f"Error releasing connection: {e}")

    def _is_expired(self, conn: Connection) -> bool:
        """Check if connection has expired."""
        now = time.time()

        # Check lifetime
        if (now - conn.created_at) > self.max_lifetime:
            return True

        # Check idle time
        if (now - conn.last_used) > self.max_idle_time:
            return True

        return False

    def _close_connection(self, conn: Connection):
        """Close and remove connection."""
        try:
            if hasattr(conn.connection, "close"):
                conn.connection.close()

            with self.lock:
                self.size -= 1

            logger.debug(f"Closed connection (pool size: {self.size})")

        except Exception as e:
            logger.error(f"Error closing connection: {e}")

    def _cleanup_loop(self):
        """Background cleanup of expired connections."""
        while True:
            time.sleep(60)  # Check every minute

            try:
                # Check connections in pool
                expired = []
                temp_queue = Queue()

                while not self.pool.empty():
                    try:
                        conn = self.pool.get_nowait()
                        if self._is_expired(conn):
                            expired.append(conn)
                        else:
                            temp_queue.put(conn)
                    except Empty:
                        break

                # Put non-expired back
                while not temp_queue.empty():
                    self.pool.put(temp_queue.get())

                # Close expired
                for conn in expired:
                    self._close_connection(conn)

                if expired:
                    logger.info(f"Cleaned up {len(expired)} expired connections")

            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")

    def stats(self) -> dict:
        """Get pool statistics."""
        return {
            "pool_size": self.size,
            "available": self.pool.qsize(),
            "in_use": self.size - self.pool.qsize(),
            "created_total": self.created_count,
            "recycled_total": self.recycled_count,
            "max_wait_time": round(self.max_wait_time, 3),
        }

    def close_all(self):
        """Close all connections in pool."""
        while not self.pool.empty():
            try:
                conn = self.pool.get_nowait()
                self._close_connection(conn)
            except Empty:
                break

        logger.info("All pool connections closed")
