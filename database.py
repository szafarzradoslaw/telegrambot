import sqlite3

DB_FILE = "food_macros.db"

def get_connection():
    """
    Create a new SQLite connection with row factory set to sqlite3.Row.
    Use this function in repositories for all database operations.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # so we can access columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # enforce foreign key constraints
    return conn
