from fastapi import APIRouter, HTTPException, Query, status
from database.connection import get_connection
from api.models.workout import WorkoutSummaryResponse, WorkoutDetailResponse
from api.models.workout_create import WorkoutCreate
from api.models.workout_update import WorkoutUpdate
from uuid import uuid4
import sqlite3

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)

@router.get("/", response_model=list[WorkoutSummaryResponse])
def get_workouts(
    limit: int = Query(default = 10, ge=1, le = 100),
    offset: int = Query(default=0, ge=0),
    title: str | None = Query(default=None)
):
    conn = get_connection()
    cursor = conn.cursor()
    if title is not None:
        search_pattern = f"%{title}%"

        cursor.execute("""
                SELECT session_id, title, start_time, end_time, description
                FROM workout_sessions
                WHERE title LIKE ?
                ORDER BY start_time DESC, session_id DESC
                LIMIT ? OFFSET ?
            """,(search_pattern,limit,offset))

    else:
        cursor.execute("""
                        SELECT session_id, title, start_time, end_time, description
                        FROM workout_sessions
                        ORDER BY start_time DESC, session_id DESC
                        LIMIT ? OFFSET ?
                    """,(limit,offset)) 

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
    LEFT JOIN workout_sets AS wst
        ON ws.session_id = wst.session_id
    LEFT JOIN exercises AS e
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
        
        if row["exercise_id"] is None:
            continue

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

@router.post("/", status_code= status.HTTP_201_CREATED)
def create_workout(workout: WorkoutCreate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO workout_sessions(hevy_session_key, title, start_time, end_time, description)
        VALUES(?,?,?,?,?)
        """,( f"manual_{uuid4().hex}",workout.title,workout.start_time,workout.end_time,workout.description))

        session_id = cursor.lastrowid

        for exercise_index, exercise in enumerate(workout.exercises):
            for set_index, workout_set in enumerate(exercise.sets):
                cursor.execute("""
                INSERT INTO workout_sets(
                session_id, 
                exercise_id,
                order_in_session, 
                set_number,
                set_type, 
                weight, 
                reps)
                VALUES(?,?,?,?,?,?,?)
                """,(session_id,
                     exercise.exercise_id,
                     exercise_index,
                     set_index,
                     workout_set.set_type,
                     workout_set.weight,
                     workout_set.reps ))

        conn.commit()
        return {
        "message": "Workout created successfully",
        "session_id": session_id
        }

    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid workout data or exercise ID"
        )
    
    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

@router.patch("/{session_id}")
def update_workout(session_id: int, workout: WorkoutUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        updates = workout.model_dump(exclude_unset=True)

        if not updates:
            raise HTTPException(
                status_code= 400,
                detail = "No fields provided for the update"
            )

        cursor.execute(
            "SELECT 1 FROM workout_sessions WHERE session_id = ?",
            (session_id,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail="Workout not found"
            )
        
        allowed_fields = {"title", "start_time", "end_time", "description"}
        if not set(updates).issubset(allowed_fields):
            raise HTTPException(
                status_code=400,
                detail="Invalid update fields"
            )
        
        set_clause = ", ".join(f"{field} = ?" for field in updates)
        
        values = list(updates.values())
        values.append(session_id)

        cursor.execute(f"""
            UPDATE workout_sessions
            SET {set_clause}
            WHERE session_id = ?
        """,values)
        
        conn.commit()

        return {"message": "Workout updated successfully"}

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(session_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT 1 FROM workout_sessions WHERE session_id = ?",
            (session_id,)
            )
        
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail="Workout not found"
                )

        cursor.execute("""
            DELETE from workout_sessions
            WHERE session_id = ?
        """,(session_id,))

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()