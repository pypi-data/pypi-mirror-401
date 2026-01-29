"""
Evolutionary Memory - Persistent storage and learning with SQL injection protection
"""

import json
import os
import sqlite3
import threading
from datetime import datetime
from typing import Any, Dict, List


def adapt_datetime(dt):
    """Convert datetime to ISO format string for SQLite"""
    return dt.isoformat()


def convert_datetime(s):
    """Convert ISO format string back to datetime"""
    if isinstance(s, bytes):
        s = s.decode("utf-8")
    return datetime.fromisoformat(s)


# Register adapters for Python 3.12+
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("DATETIME", convert_datetime)
sqlite3.register_converter("TIMESTAMP", convert_datetime)


class EvolutionaryMemory:
    """Stores and learns from system history with secure database operations"""

    def __init__(self, db_path: str = "entropy_memory.db", use_postgres: bool = False):
        """
        Initialize memory storage.

        Args:
            db_path: Path to SQLite database or PostgreSQL connection string
            use_postgres: Whether to use PostgreSQL instead of SQLite
        """
        self.use_postgres = use_postgres or os.getenv("DATABASE_URL")
        self._lock = threading.RLock()

        if self.use_postgres:
            self._init_postgres()
        else:
            self.db_path = db_path
            self.conn = sqlite3.connect(
                db_path,
                check_same_thread=False,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )
            self.conn.row_factory = sqlite3.Row

        self._create_tables()

    def _init_postgres(self):
        """Initialize PostgreSQL connection"""
        import psycopg2
        from psycopg2.extras import RealDictCursor

        db_url = os.getenv("DATABASE_URL", "postgresql://localhost/entropic")
        self.conn = psycopg2.connect(db_url)
        self.conn.cursor_factory = RealDictCursor

    def _create_tables(self):
        """Creates database schema with proper SQL"""
        cursor = self.conn.cursor()

        # Events table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                entropy_value REAL NOT NULL,
                event_type TEXT NOT NULL,
                agents_involved TEXT,
                action_taken TEXT,
                outcome TEXT,
                metadata TEXT
            )
        """
            if self.use_postgres
            else """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                entropy_value REAL NOT NULL,
                event_type TEXT NOT NULL,
                agents_involved TEXT,
                action_taken TEXT,
                outcome TEXT,
                metadata TEXT
            )
        """
        )

        # Patterns table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS patterns (
                id SERIAL PRIMARY KEY,
                pattern_hash TEXT UNIQUE NOT NULL,
                description TEXT,
                conditions TEXT NOT NULL,
                success_rate REAL DEFAULT 0.0,
                usage_count INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                created_at TIMESTAMP NOT NULL
            )
        """
            if self.use_postgres
            else """
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_hash TEXT UNIQUE NOT NULL,
                description TEXT,
                conditions TEXT NOT NULL,
                success_rate REAL DEFAULT 0.0,
                usage_count INTEGER DEFAULT 0,
                last_used DATETIME,
                created_at DATETIME NOT NULL
            )
        """
        )

        # Rules table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rules (
                id SERIAL PRIMARY KEY,
                condition TEXT NOT NULL,
                action TEXT NOT NULL,
                effectiveness REAL DEFAULT 0.5,
                times_applied INTEGER DEFAULT 0,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """
            if self.use_postgres
            else """
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                condition TEXT NOT NULL,
                action TEXT NOT NULL,
                effectiveness REAL DEFAULT 0.5,
                times_applied INTEGER DEFAULT 0,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            )
        """
        )

        # Metrics table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metrics (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                entropy_combined REAL,
                entropy_decision REAL,
                entropy_dispersion REAL,
                entropy_communication REAL,
                agent_count INTEGER,
                system_state TEXT
            )
        """
            if self.use_postgres
            else """
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                entropy_combined REAL,
                entropy_decision REAL,
                entropy_dispersion REAL,
                entropy_communication REAL,
                agent_count INTEGER,
                system_state TEXT
            )
        """
        )

        self.conn.commit()

    def log_event(
        self,
        entropy: float,
        event_type: str,
        action: str = None,
        outcome: str = None,
        metadata: Dict = None,
    ) -> int:
        """
        Logs a significant event using parameterized queries.

        Args:
            entropy: Current entropy value
            event_type: Type of event
            action: Action taken
            outcome: Result of action
            metadata: Additional metadata

        Returns:
            Event ID
        """
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(
                (
                    """
                INSERT INTO events (timestamp, entropy_value, event_type, action_taken, outcome, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """
                    if not self.use_postgres
                    else """
                INSERT INTO events (timestamp, entropy_value, event_type, action_taken, outcome, metadata)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """
                ),
                (
                    datetime.now(),
                    float(entropy),
                    str(event_type),
                    str(action) if action else None,
                    str(outcome) if outcome else None,
                    json.dumps(metadata) if metadata else None,
                ),
            )

            self.conn.commit()
            return (
                cursor.lastrowid if not self.use_postgres else cursor.fetchone()["id"]
            )

    def log_decision(
        self, entropy: float, action: str, result: str = None, metadata: Dict = None
    ) -> int:
        """
        Logs a regulation decision (alias for log_event for backward compatibility).

        Args:
            entropy: Current entropy value
            action: Action taken by regulator
            result: Result of the action ('success', 'failure', etc.)
            metadata: Additional metadata

        Returns:
            Event ID
        """
        return self.log_event(
            entropy=entropy,
            event_type="regulation",
            action=action,
            outcome=result,
            metadata=metadata,
        )

    def log_metrics(self, metrics: Dict[str, Any], agent_count: int) -> None:
        """Logs entropy metrics using parameterized queries"""
        with self._lock:
            cursor = self.conn.cursor()

            try:
                cursor.execute(
                    (
                        """
                    INSERT INTO metrics (timestamp, entropy_combined, entropy_decision, 
                                       entropy_dispersion, entropy_communication, agent_count)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                        if not self.use_postgres
                        else """
                    INSERT INTO metrics (timestamp, entropy_combined, entropy_decision, 
                                       entropy_dispersion, entropy_communication, agent_count)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                    ),
                    (
                        datetime.now(),
                        metrics.get("combined"),
                        metrics.get("decision"),
                        metrics.get("dispersion"),
                        metrics.get("communication"),
                        int(agent_count),
                    ),
                )
                self.conn.commit()
            except Exception as e:
                # Handle thread safety issues with SQLite
                import logging

                logging.getLogger(__name__).debug(f"Error logging metrics: {e}")
                try:
                    self.conn.rollback()
                except:
                    pass

    def get_recent_events(self, limit: int = 10, event_type: str = None) -> List[Dict]:
        """
        Retrieves recent events using parameterized queries.

        Args:
            limit: Maximum number of events
            event_type: Optional filter by event type

        Returns:
            List of event dictionaries
        """
        cursor = self.conn.cursor()

        if event_type:
            cursor.execute(
                (
                    """
                SELECT timestamp, entropy_value, event_type, action_taken, outcome, metadata
                FROM events
                WHERE event_type = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """
                    if not self.use_postgres
                    else """
                SELECT timestamp, entropy_value, event_type, action_taken, outcome, metadata
                FROM events
                WHERE event_type = %s
                ORDER BY timestamp DESC
                LIMIT %s
            """
                ),
                (str(event_type), int(limit)),
            )
        else:
            cursor.execute(
                (
                    """
                SELECT timestamp, entropy_value, event_type, action_taken, outcome, metadata
                FROM events
                ORDER BY timestamp DESC
                LIMIT ?
            """
                    if not self.use_postgres
                    else """
                SELECT timestamp, entropy_value, event_type, action_taken, outcome, metadata
                FROM events
                ORDER BY timestamp DESC
                LIMIT %s
            """
                ),
                (int(limit),),
            )

        results = []
        for row in cursor.fetchall():
            results.append(
                {
                    "timestamp": row["timestamp"] if isinstance(row, dict) else row[0],
                    "entropy": (
                        row["entropy_value"] if isinstance(row, dict) else row[1]
                    ),
                    "type": row["event_type"] if isinstance(row, dict) else row[2],
                    "action": row["action_taken"] if isinstance(row, dict) else row[3],
                    "outcome": row["outcome"] if isinstance(row, dict) else row[4],
                    "metadata": (
                        json.loads(row["metadata"])
                        if (row["metadata"] if isinstance(row, dict) else row[5])
                        else None
                    ),
                }
            )

        return results

    def query_events(self, limit: int = None, event_type: str = None) -> List[Dict]:
        """
        Query events (alias for get_recent_events for backward compatibility).

        Args:
            limit: Maximum number of events
            event_type: Optional filter by event type

        Returns:
            List of event dictionaries
        """
        return self.get_recent_events(limit=limit or 10, event_type=event_type)

    def get_metrics_history(self, hours: int = 24) -> List[Dict]:
        """Retrieves metrics history using parameterized queries"""
        cursor = self.conn.cursor()
        cursor.execute(
            (
                """
            SELECT timestamp, entropy_combined, entropy_decision, entropy_dispersion, 
                   entropy_communication, agent_count
            FROM metrics
            WHERE timestamp >= datetime('now', '-' || ? || ' hours')
            ORDER BY timestamp ASC
        """
                if not self.use_postgres
                else """
            SELECT timestamp, entropy_combined, entropy_decision, entropy_dispersion, 
                   entropy_communication, agent_count
            FROM metrics
            WHERE timestamp >= NOW() - INTERVAL '%s hours'
            ORDER BY timestamp ASC
        """
            ),
            (int(hours),),
        )

        results = []
        for row in cursor.fetchall():
            results.append(
                {
                    "timestamp": row["timestamp"] if isinstance(row, dict) else row[0],
                    "combined": (
                        row["entropy_combined"] if isinstance(row, dict) else row[1]
                    ),
                    "decision": (
                        row["entropy_decision"] if isinstance(row, dict) else row[2]
                    ),
                    "dispersion": (
                        row["entropy_dispersion"] if isinstance(row, dict) else row[3]
                    ),
                    "communication": (
                        row["entropy_communication"]
                        if isinstance(row, dict)
                        else row[4]
                    ),
                    "agent_count": (
                        row["agent_count"] if isinstance(row, dict) else row[5]
                    ),
                }
            )

        return results

    def search_events(self, query: str, limit: int = 100) -> List[Dict]:
        """
        Search events by query string using parameterized queries.

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of matching events
        """
        cursor = self.conn.cursor()

        # Sanitize query - use parameterized query
        search_pattern = f"%{query}%"

        cursor.execute(
            (
                """
            SELECT timestamp, entropy_value, event_type, action_taken, outcome, metadata
            FROM events
            WHERE event_type LIKE ? OR action_taken LIKE ? OR outcome LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """
                if not self.use_postgres
                else """
            SELECT timestamp, entropy_value, event_type, action_taken, outcome, metadata
            FROM events
            WHERE event_type LIKE %s OR action_taken LIKE %s OR outcome LIKE %s
            ORDER BY timestamp DESC
            LIMIT %s
        """
            ),
            (search_pattern, search_pattern, search_pattern, int(limit)),
        )

        results = []
        for row in cursor.fetchall():
            results.append(
                {
                    "timestamp": row["timestamp"] if isinstance(row, dict) else row[0],
                    "entropy": (
                        row["entropy_value"] if isinstance(row, dict) else row[1]
                    ),
                    "type": row["event_type"] if isinstance(row, dict) else row[2],
                    "action": row["action_taken"] if isinstance(row, dict) else row[3],
                    "outcome": row["outcome"] if isinstance(row, dict) else row[4],
                    "metadata": (
                        json.loads(row["metadata"])
                        if (row["metadata"] if isinstance(row, dict) else row[5])
                        else None
                    ),
                }
            )

        return results

    def find_similar_patterns(
        self, pattern: Dict[str, Any], limit: int = 5
    ) -> List[Dict]:
        """
        Find similar patterns in memory (simplified implementation).

        Args:
            pattern: Pattern dictionary to search for
            limit: Maximum number of results

        Returns:
            List of similar patterns
        """
        # Simple implementation - return recent events that match pattern criteria
        cursor = self.conn.cursor()
        cursor.execute(
            (
                """
            SELECT timestamp, entropy_value, event_type, action_taken, outcome, metadata
            FROM events
            ORDER BY timestamp DESC
            LIMIT ?
        """
                if not self.use_postgres
                else """
            SELECT timestamp, entropy_value, event_type, action_taken, outcome, metadata
            FROM events
            ORDER BY timestamp DESC
            LIMIT %s
        """
            ),
            (int(limit),),
        )

        results = []
        for row in cursor.fetchall():
            results.append(
                {
                    "timestamp": row["timestamp"] if isinstance(row, dict) else row[0],
                    "entropy": (
                        row["entropy_value"] if isinstance(row, dict) else row[1]
                    ),
                    "type": row["event_type"] if isinstance(row, dict) else row[2],
                    "action": row["action_taken"] if isinstance(row, dict) else row[3],
                    "outcome": row["outcome"] if isinstance(row, dict) else row[4],
                    "metadata": (
                        json.loads(row["metadata"])
                        if (row["metadata"] if isinstance(row, dict) else row[5])
                        else None
                    ),
                }
            )

        return results

    def query_patterns(
        self, min_success_rate: float = 0.0, limit: int = 100
    ) -> List[Dict]:
        """
        Query stored patterns by success rate.

        Args:
            min_success_rate: Minimum success rate filter (0.0 to 1.0)
            limit: Maximum number of patterns to return

        Returns:
            List of pattern dictionaries
        """
        cursor = self.conn.cursor()
        cursor.execute(
            (
                """
            SELECT id, pattern_hash, description, conditions, success_rate, usage_count, last_used, created_at
            FROM patterns
            WHERE success_rate >= ?
            ORDER BY success_rate DESC, usage_count DESC
            LIMIT ?
        """
                if not self.use_postgres
                else """
            SELECT id, pattern_hash, description, conditions, success_rate, usage_count, last_used, created_at
            FROM patterns
            WHERE success_rate >= %s
            ORDER BY success_rate DESC, usage_count DESC
            LIMIT %s
        """
            ),
            (float(min_success_rate), int(limit)),
        )

        results = []
        for row in cursor.fetchall():
            results.append(
                {
                    "id": row["id"] if isinstance(row, dict) else row[0],
                    "pattern_hash": (
                        row["pattern_hash"] if isinstance(row, dict) else row[1]
                    ),
                    "description": (
                        row["description"] if isinstance(row, dict) else row[2]
                    ),
                    "conditions": (
                        json.loads(
                            row["conditions"] if isinstance(row, dict) else row[3]
                        )
                        if (row["conditions"] if isinstance(row, dict) else row[3])
                        else {}
                    ),
                    "success_rate": (
                        row["success_rate"] if isinstance(row, dict) else row[4]
                    ),
                    "usage_count": (
                        row["usage_count"] if isinstance(row, dict) else row[5]
                    ),
                    "last_used": row["last_used"] if isinstance(row, dict) else row[6],
                    "created_at": (
                        row["created_at"] if isinstance(row, dict) else row[7]
                    ),
                }
            )

        return results

    def store_pattern(
        self,
        pattern_hash: str,
        conditions: Dict,
        description: str = None,
        success_rate: float = 0.0,
    ) -> int:
        """
        Store a new pattern in memory.

        Args:
            pattern_hash: Unique identifier for the pattern
            conditions: Pattern conditions dictionary
            description: Human-readable description
            success_rate: Initial success rate

        Returns:
            Pattern ID
        """
        with self._lock:
            cursor = self.conn.cursor()
            now = datetime.now()

            try:
                cursor.execute(
                    (
                        """
                    INSERT INTO patterns (pattern_hash, description, conditions, success_rate, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """
                        if not self.use_postgres
                        else """
                    INSERT INTO patterns (pattern_hash, description, conditions, success_rate, created_at)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """
                    ),
                    (
                        str(pattern_hash),
                        str(description) if description else None,
                        json.dumps(conditions),
                        float(success_rate),
                        now,
                    ),
                )
                self.conn.commit()
                return (
                    cursor.lastrowid
                    if not self.use_postgres
                    else cursor.fetchone()["id"]
                )
            except sqlite3.IntegrityError:
                # Pattern already exists, update it
                cursor.execute(
                    (
                        """
                    UPDATE patterns 
                    SET usage_count = usage_count + 1, last_used = ?
                    WHERE pattern_hash = ?
                """
                        if not self.use_postgres
                        else """
                    UPDATE patterns 
                    SET usage_count = usage_count + 1, last_used = %s
                    WHERE pattern_hash = %s
                """
                    ),
                    (now, str(pattern_hash)),
                )
                self.conn.commit()
                return -1

    def close(self):
        """Closes database connection properly to release file locks"""
        if self.conn:
            try:
                self.conn.commit()
            except Exception:
                pass

            try:
                self.conn.close()
            except Exception:
                pass

            self.conn = None
