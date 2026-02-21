"""Database schema setup and initialization."""
import sqlite3
from typing import Optional
from .connection import DatabaseConnection


class DatabaseSchema:
    """Manages database schema and initialization."""
    
    USER_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    CALORIES_TABLE = """
    CREATE TABLE IF NOT EXISTS calories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        calories REAL NOT NULL,
        food_name TEXT,
        food_type TEXT,
        quantity REAL,
        unit TEXT,
        source TEXT CHECK(source IN ('label', 'estimate')),
        image_path TEXT,
        notes TEXT,
        logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """
    
    @staticmethod
    def initialize_database(db: DatabaseConnection):
        """Initialize database schema."""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Create tables
            cursor.execute(DatabaseSchema.USER_TABLE)
            cursor.execute(DatabaseSchema.CALORIES_TABLE)
            
            # Create indexes for faster queries
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_calories_user_id ON calories(user_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_calories_logged_at ON calories(logged_at)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)"
            )
            
            conn.commit()
            print("Database schema initialized successfully.")
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Database initialization error: {e}")
            raise
