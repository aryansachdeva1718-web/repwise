from fastapi import APIRouter
from database.connection import get_connection
from api.models.workout import WorkoutResponse

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)


@router.get("/", response_model=list[WorkoutResponse])
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
