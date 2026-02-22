"""Database module for Calorie Tracker."""
import sqlite3
import os
from typing import Optional


class DatabaseConnection:
    """Manages database connection and operations."""
    
    def __init__(self, db_path: str = "calories.db"):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
    
    def connect(self):
        """Establish database connection."""
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def get_connection(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self.connection is None:
            self.connect()
        return self.connection
    
    def execute(self, query: str, params: tuple = ()):
        """Execute a query."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    
    def fetch_one(self, query: str, params: tuple = ()):
        """Fetch a single row."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
    
    def fetch_all(self, query: str, params: tuple = ()):
        """Fetch all rows."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()


# Global database instance
_db: Optional[DatabaseConnection] = None


def get_database(db_path: str = "calories.db") -> DatabaseConnection:
    """Get global database instance."""
    global _db
    if _db is None:
        _db = DatabaseConnection(db_path)
    return _db
