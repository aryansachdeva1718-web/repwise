from fastapi import APIRouter, HTTPException
from database.connection import get_connection
from api.models.workout import WorkoutSummaryResponse, WorkoutDetailResponse

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)


@router.get("/", response_model=list[WorkoutSummaryResponse])
def get_workouts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT session_id, title, start_time, end_time, description
        FROM workout_sessions
        ORDER BY start_time DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

@router.get("/{session_id}", response_model=WorkoutDetailResponse)
def get_workout(session_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        ws.session_id, ws.title, ws.start_time, ws.end_time, ws.description, 
        e.exercise_id, e.name, 
        wst.set_number, wst.set_type, wst.weight, wst.reps, wst.rpe
    FROM workout_sessions as ws
    JOIN workout_sets as wst
        ON ws.session_id = wst.session_id
    JOIN exercises as e
        ON wst.exercise_id = e.exercise_id
    WHERE ws.session_id = ?
    ORDER BY wst.order_in_session,wst.set_number""", (session_id,))

    e_rows = cursor.fetchall()
    conn.close()

    if not e_rows:
        raise HTTPException(
            status_code= 404,
            detail = "Workout not found for this id"
        )

    first_row = e_rows[0]
    workout = {
        "session_id": first_row["session_id"],
        "title": first_row["title"],
        "start_time": first_row["start_time"],
        "end_time": first_row["end_time"],
        "description": first_row["description"],
        "exercises": []
    }

    exercises = {}
    for row in e_rows:

        exercise_id = row["exercise_id"]

        if exercise_id not in exercises:
            exercises[exercise_id] = {
                "exercise_id": row["exercise_id"],
                "name": row["name"],
                "sets": []
            }

        set_data = {
            "set_number": row["set_number"],
            "set_type": row["set_type"],
            "weight": row["weight"],
            "reps": row["reps"],
            "rpe": row["rpe"]
        }

        exercises[exercise_id]["sets"].append(set_data)

    workout["exercises"] = list(exercises.values())

    return workout

    

