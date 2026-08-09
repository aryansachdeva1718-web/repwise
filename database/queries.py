import pandas as pd
import uuid
from database.connection import get_connection

def get_workout_dates():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT start_time
        FROM workout_sessions
        ORDER BY start_time;
    """)

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]

def get_workout_details(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ws.set_id,
            ws.session_id,
            e.name AS exercise,
            ws.set_number,
            ws.set_type,
            ws.weight,
            ws.reps,
            ws.distance_km,
            ws.duration_seconds,
            ws.rpe
        FROM workout_sets ws
        JOIN exercises e
            ON ws.exercise_id = e.exercise_id
        WHERE ws.session_id = ?
        ORDER BY ws.order_in_session;
    """, (session_id,))

    rows = cursor.fetchall()

    columns = [
        "Set_ID",
        "Session_ID",
        "Exercise",
        "Set",
        "Set_Type",
        "Weight",
        "Reps",
        "Distance_KM",
        "Duration_Seconds",
        "RPE"
    ]

    conn.close()

    return pd.DataFrame(rows, columns=columns)

def get_workout_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ws.set_id,
            ws.session_id,
            DATE(ws_session.start_time) AS date,
            e.name AS exercise,
            ws.set_number,
            ws.set_type,
            ws.weight,
            ws.reps,
            ws.distance_km,
            ws.duration_seconds,
            ws.rpe
        FROM workout_sets ws
        JOIN workout_sessions ws_session
            ON ws.session_id = ws_session.session_id
        JOIN exercises e
            ON ws.exercise_id = e.exercise_id
        ORDER BY ws_session.start_time, ws.order_in_session;
    """)

    rows = cursor.fetchall()

    columns = [
        "Set_ID",
        "Session_ID",
        "Date",
        "Exercise",
        "Set",
        "Set_Type",
        "Weight",
        "Reps",
        "Distance_KM",
        "Duration_Seconds",
        "RPE"
    ]

    conn.close()

    return pd.DataFrame(rows, columns=columns)

def get_recent_workouts(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            session_id,
            title,
            start_time,
            end_time,
            description
        FROM workout_sessions
        ORDER BY start_time DESC
        LIMIT ?;
    """, (limit,))

    rows = cursor.fetchall()

    columns = [
        "Session_ID",
        "Title",
        "Start_Time",
        "End_Time",
        "Description"
    ]

    conn.close()

    return pd.DataFrame(rows, columns=columns)

def get_exercise_history(exercise):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            DATE(ws_session.start_time) AS date,
            e.name AS exercise,
            ws.set_number,
            ws.set_type,
            ws.weight,
            ws.reps,
            ws.distance_km,
            ws.duration_seconds,
            ws.rpe
        FROM workout_sets ws
        JOIN workout_sessions ws_session
            ON ws.session_id = ws_session.session_id
        JOIN exercises e
            ON ws.exercise_id = e.exercise_id
        WHERE e.name = ?
        ORDER BY ws_session.start_time, ws.order_in_session;
    """, (exercise,))

    rows = cursor.fetchall()

    columns = [
        "Date",
        "Exercise",
        "Set",
        "Set_Type",
        "Weight",
        "Reps",
        "Distance_KM",
        "Duration_Seconds",
        "RPE"
    ]

    conn.close()

    return pd.DataFrame(rows, columns=columns)

def get_daily_metrics(date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            date,
            sleep,
            calories,
            bodyweight
        FROM daily_metrics
        WHERE date = ?;
    """, (date,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "Date": row[0],
        "Sleep": row[1],
        "Calories": row[2],
        "Bodyweight": row[3]
    }

def get_exercise_id(exercise_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT exercise_id
        FROM exercises
        WHERE name = ?;
    """, (exercise_name,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return row[0]


def create_workout_session(
    cursor,
    title,
    start_time,
    end_time=None,
    description=None,
    hevy_session_key=None
):
    if hevy_session_key is None:
        hevy_session_key = f"repwise_{uuid.uuid4()}"

    cursor.execute("""
        INSERT INTO workout_sessions (
            hevy_session_key,
            title,
            start_time,
            end_time,
            description
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        hevy_session_key,
        title,
        start_time,
        end_time,
        description
    ))

    return cursor.lastrowid


def add_workout_set(
    cursor,
    session_id,
    exercise_id,
    order_in_session,
    set_number,
    set_type="normal",
    weight=None,
    reps=None,
    distance_km=None,
    duration_seconds=None,
    superset_id=None,
    exercise_notes=None,
    rpe=None
):
    cursor.execute("""
        INSERT INTO workout_sets (
            session_id,
            exercise_id,
            order_in_session,
            set_number,
            set_type,
            weight,
            reps,
            distance_km,
            duration_seconds,
            superset_id,
            exercise_notes,
            rpe
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        session_id,
        exercise_id,
        order_in_session,
        set_number,
        set_type,
        weight,
        reps,
        distance_km,
        duration_seconds,
        superset_id,
        exercise_notes,
        rpe
    ))

    return cursor.lastrowid


def save_workout_session(
    title,
    start_time,
    exercises,
    end_time=None,
    description=None
):
    conn = get_connection()
    cursor = conn.cursor()

    pr_messages = []

    try:
        # Create the workout session
        session_id = create_workout_session(
            cursor=cursor,
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description
        )

        # Keep track of the overall order of sets
        order_in_session = 1

        for exercise_data in exercises:

            exercise_name = exercise_data["exercise"]
            reps_list = exercise_data["reps"]
            weight_list = exercise_data["weights"]

            exercise_id = get_exercise_id_from_cursor(
                cursor,
                exercise_name
            )

            if exercise_id is None:
                raise ValueError(
                    f"Exercise not found in database: {exercise_name}"
                )

            # Find previous maximum weight for PR checking
            cursor.execute("""
                SELECT MAX(ws.weight)
                FROM workout_sets ws
                JOIN exercises e
                    ON ws.exercise_id = e.exercise_id
                WHERE e.name = ?;
            """, (exercise_name,))

            row = cursor.fetchone()
            max_weight = row[0] if row[0] is not None else 0

            for set_number, (reps, weight) in enumerate(
                zip(reps_list, weight_list),
                start=1
            ):

                if weight > max_weight:

                    if max_weight == 0:
                        pr_messages.append(
                            f"🏆 Starting PR for {exercise_name}: "
                            f"{weight} kg"
                        )
                    else:
                        pr_messages.append(
                            f"🏆 New {exercise_name} PR: "
                            f"Previous {max_weight} kg → "
                            f"Current {weight} kg"
                        )

                    # Update max so multiple sets in the same workout
                    # don't repeatedly report the same PR.
                    max_weight = weight

                add_workout_set(
                    cursor=cursor,
                    session_id=session_id,
                    exercise_id=exercise_id,
                    order_in_session=order_in_session,
                    set_number=set_number,
                    set_type="normal",
                    weight=weight,
                    reps=reps
                )

                order_in_session += 1

        # Everything succeeded
        conn.commit()

        return session_id, pr_messages

    except Exception:
        # Anything fails → entire workout is cancelled
        conn.rollback()
        raise

    finally:
        conn.close()


def get_exercise_id_from_cursor(cursor, exercise_name):
    cursor.execute("""
        SELECT exercise_id
        FROM exercises
        WHERE name = ?;
    """, (exercise_name,))

    row = cursor.fetchone()

    if row is None:
        return None

    return row[0]


def save_daily_metrics(date, sleep, calories, bodyweight):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO daily_metrics (
            date,
            sleep,
            calories,
            bodyweight
        )
        VALUES (?, ?, ?, ?);
    """, (
        date,
        sleep,
        calories,
        bodyweight
    ))

    conn.commit()
    conn.close()