import os
import sqlite3

def get_connection():
    db_path = os.getenv("REPWISE_DB_PATH", "data/repwise.db") # If REPWISE_DB_PATH exists, use its value; otherwise, use the normal data/repwise.db.

    conn = sqlite3.connect("data/repwise.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn