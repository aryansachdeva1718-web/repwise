from database.connection import get_connection
from database.queries import (
    create_workout_session,
    add_workout_set,
    get_exercise_id_from_cursor
)


def test_successful_transaction():

    print("\n--- Successful Transaction Test ---")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Create a test session
        session_id = create_workout_session(
            cursor=cursor,
            title="Transaction Test",
            start_time="2026-08-09 20:00:00",
            end_time="2026-08-09 20:30:00"
        )

        print(f"Created session: {session_id}")

        # 2. Get an existing exercise
        exercise_id = get_exercise_id_from_cursor(
            cursor,
            "Shoulder Press (Dumbbell)"
        )

        print(f"Exercise ID: {exercise_id}")

        if exercise_id is None:
            raise ValueError("Test exercise was not found.")

        # 3. Insert two sets
        set_1 = add_workout_set(
            cursor=cursor,
            session_id=session_id,
            exercise_id=exercise_id,
            order_in_session=1,
            set_number=1,
            weight=50,
            reps=10
        )

        set_2 = add_workout_set(
            cursor=cursor,
            session_id=session_id,
            exercise_id=exercise_id,
            order_in_session=2,
            set_number=2,
            weight=50,
            reps=8
        )

        print(f"Created sets: {set_1}, {set_2}")

        # 4. Commit the entire transaction
        conn.commit()

        print("Transaction committed successfully.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def test_rollback():

    print("\n--- Rollback Test ---")

    conn = get_connection()
    cursor = conn.cursor()

    session_id = None

    try:
        # 1. Create session
        session_id = create_workout_session(
            cursor=cursor,
            title="Rollback Test",
            start_time="2026-08-09 21:00:00"
        )

        print(f"Created temporary session: {session_id}")

        # 2. Get exercise
        exercise_id = get_exercise_id_from_cursor(
            cursor,
            "Shoulder Press (Dumbbell)"
        )

        # 3. Insert a set
        add_workout_set(
            cursor=cursor,
            session_id=session_id,
            exercise_id=exercise_id,
            order_in_session=1,
            set_number=1,
            weight=50,
            reps=10
        )

        print("Inserted temporary set.")

        # 4. Deliberately cause an error
        raise Exception("Intentional test failure")

    except Exception as e:

        print(f"Error occurred: {e}")
        print("Rolling back transaction...")

        conn.rollback()

    finally:
        conn.close()


if __name__ == "__main__":

    test_successful_transaction()

    test_rollback()

    print("\nTransaction tests completed.")