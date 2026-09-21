import sqlite3
import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# DATABASE PATH
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "repwise.db"




# ---------------------------------------------------------
# LOAD RAW WORKOUT DATA
# ---------------------------------------------------------

def load_workout_data():

    query = """
        SELECT
            ws.session_id,
            ws.start_time,
            wset.exercise_id,
            e.name AS exercise_name,
            wset.set_number,
            wset.set_type,
            wset.weight,
            wset.reps,
            wset.rpe

        FROM workout_sessions AS ws

        JOIN workout_sets AS wset
            ON ws.session_id = wset.session_id

        JOIN exercises AS e
            ON wset.exercise_id = e.exercise_id

        ORDER BY
            ws.start_time,
            wset.exercise_id,
            wset.set_number
    """

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)

    return df

def build_exercise_dataset():

    df = load_workout_data()

    if df.empty:
        return df

    # Convert date/time
    df["start_time"] = pd.to_datetime(df["start_time"])

    # Date of workout
    df["session_date"] = df["start_time"].dt.date

    # Ignore sets where weight or reps are missing
    df = df.dropna(
        subset=["weight", "reps"]
    )

    # Calculate set volume
    df["set_volume"] = (
        df["weight"] * df["reps"]
    )

    # Estimated 1RM for each set
    df["set_e1rm"] = (
        df["weight"] *
        (1 + df["reps"] / 30)
    )

    # Aggregate sets into exercise-session rows
    exercise_sessions = (
        df
        .groupby(
            [
                "session_id",
                "session_date",
                "exercise_id",
                "exercise_name"
            ]
        )
        .agg(
            sets=("set_number", "count"),
            total_reps=("reps", "sum"),
            total_volume=("set_volume", "sum"),
            best_weight=("weight", "max"),
            best_e1rm=("set_e1rm", "max"),
            average_rpe=("rpe", "mean")
        )
        .reset_index()
    )

    return exercise_sessions

