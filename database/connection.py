
import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PRODUCTION_DB = (BASE_DIR / "data" / "repwise.db").resolve()
TEST_DB = (BASE_DIR / "data" / "repwise_test.db").resolve()


def get_connection():
    # Development is the default for safety.
    app_env = os.getenv("REPWISE_ENV", "development").lower()

    if app_env not in ("development", "production"):
        raise RuntimeError(
            f"Invalid REPWISE_ENV: {app_env}"
        )

    # Choose database based on the environment.
    default_db = TEST_DB if app_env == "development" else PRODUCTION_DB

    db_path = os.getenv("REPWISE_DB_PATH")
    selected_db = Path(db_path).resolve() if db_path else default_db

    # Prevent development from accessing production.
    if app_env == "development" and selected_db != TEST_DB:
        raise RuntimeError(
            "Development mode must use repwise_test.db"
        )

    # Require explicit production database selection.
    if app_env == "production" and selected_db != PRODUCTION_DB:
        raise RuntimeError(
            "Production mode must use repwise.db"
        )

    # Prevent SQLite from silently creating a new database.
    if not selected_db.is_file():
        raise FileNotFoundError(
            f"Database not found: {selected_db}"
        )

    # Read/write existing database.
    uri = selected_db.as_uri() + "?mode=rw"

    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn
