# SQLite database configuration using sqlite3 (no ORM overhead)
import sqlite3

from config import Config
from utils.logger import logger


class Database:
    """SQLite database connection and operations."""

    def __init__(self, database_url: str = Config.DATABASE_URL):
        """Initialize database connection.

        Special case: for SQLite in-memory DB (`sqlite:///:memory:`), we must reuse
        the same connection across calls; otherwise tables created during init
        won't exist in subsequent connections.
        """
        self.database_path = database_url.replace("sqlite:///", "")
        self._shared_connection: sqlite3.Connection | None = None

        if self.database_path == ":memory:":
            self._shared_connection = sqlite3.connect(":memory:")
            self._shared_connection.row_factory = sqlite3.Row

        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        if self._shared_connection is not None:
            return self._shared_connection

        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn

    def init_db(self) -> None:
        """Create all tables if not exist."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table - store user preferences
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                language TEXT DEFAULT 'en',
                notifications_enabled INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Price history table - store price data for charts
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_type TEXT NOT NULL,
                asset_name TEXT NOT NULL,
                price REAL NOT NULL,
                currency TEXT DEFAULT 'IRR',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # User alerts table - price alerts
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                asset_type TEXT NOT NULL,
                asset_name TEXT NOT NULL,
                target_price REAL NOT NULL,
                condition TEXT NOT NULL,
                currency TEXT DEFAULT 'IRR',
                is_active INTEGER DEFAULT 1,
                triggered_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """
        )

        # Create indexes for faster queries
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_price_asset
            ON price_history(asset_type, asset_name)
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_user_alerts
            ON user_alerts(user_id, is_active)
        """
        )

        conn.commit()
        logger.info("Database initialized successfully")

        # Only close if we created a new connection (not shared in-memory DB)
        if self._shared_connection is None:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> list:
        """Execute a query that returns results."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Exception as e:
            logger.error(f"Database query error: {e}")
            return []
        finally:
            if self._shared_connection is None:
                conn.close()

    def execute_update(self, query: str, params: tuple = ()) -> None:
        """Execute insert/update/delete query."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            logger.info(f"Query executed - rows affected: {cursor.rowcount}")
        except Exception as e:
            conn.rollback()
            logger.error(f"Database update error: {e}")
        finally:
            if self._shared_connection is None:
                conn.close()

    def close(self) -> None:
        """Close database connection."""
        logger.info("Database connection closed")
        if self._shared_connection is not None:
            self._shared_connection.close()
            self._shared_connection = None


# Create global database instance
db = Database()
