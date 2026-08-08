from database.connection import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Exercises Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        primary_muscle TEXT,
        secondary_muscle TEXT
    );
    """)

    # Workout Sessions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hevy_session_key TEXT UNIQUE NOT NULL,
        title TEXT,
        start_time TEXT NOT NULL,
        end_time TEXT,
        description TEXT
    );
    """)

    # Workout Sets Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_sets (
        set_id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        exercise_id INTEGER NOT NULL,
        order_in_session INTEGER NOT NULL,
        set_number INTEGER NOT NULL,
        set_type TEXT,
        weight REAL,
        reps INTEGER,
        distance_km REAL,
        duration_seconds INTEGER,
        superset_id TEXT,
        exercise_notes TEXT,
        rpe REAL,

        FOREIGN KEY (session_id)
            REFERENCES workout_sessions(session_id)
            ON DELETE CASCADE,

        FOREIGN KEY (exercise_id)
            REFERENCES exercises(exercise_id)
            ON DELETE RESTRICT
    );
    """)

    # Daily Metrics Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_metrics (
        date TEXT PRIMARY KEY,
        sleep REAL,
        calories INTEGER,
        bodyweight REAL
    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_workout_sets_exercise
    ON workout_sets(exercise_id);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_workout_sets_session
    ON workout_sets(session_id);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_sessions_start
    ON workout_sessions(start_time);
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("RepWise database schema created successfully!")