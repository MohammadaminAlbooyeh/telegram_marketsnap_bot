# SQLite database configuration using sqlite3 (no ORM overhead)
import sqlite3
import os
from app.core.config import Config
from app.core.logger import logger

class Database:
    """SQLite database connection and operations"""
    
    def __init__(self, database_url: str = Config.DATABASE_URL):
        """Initialize database connection"""
        self.database_path = database_url.replace("sqlite:///", "")
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def init_db(self):
        """Create all tables if not exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table - store user preferences
        cursor.execute("""
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
        """)
        
        # Price history table - store price data for charts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_type TEXT NOT NULL,
                asset_name TEXT NOT NULL,
                price REAL NOT NULL,
                currency TEXT DEFAULT 'IRR',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User alerts table - price alerts
        cursor.execute("""
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
        """)
        
        # Create indexes for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_price_asset 
            ON price_history(asset_type, asset_name)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_alerts 
            ON user_alerts(user_id, is_active)
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def execute_query(self, query: str, params: tuple = ()):
        """Execute a query that returns results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def execute_update(self, query: str, params: tuple = ()):
        """Execute insert/update/delete query"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        logger.info(f"Query executed - rows affected: {cursor.rowcount}")
    
    def close(self):
        """Close database connection"""
        logger.info("Database connection closed")

# Create global database instance
db = Database()