from fastapi import APIRouter, HTTPException, Query
from database.connection import get_connection
from api.models.exercise import ExerciseSummaryResponse

router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"]
)

@router.get("/", response_model = list[ExerciseSummaryResponse])
def get_exercises(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default =0, ge=0),
    name: str | None =  Query(default = None)
):
    conn = get_connection()
    cursor = conn.cursor()

    if name is not None:
        ex_name = f"%{name}%"
        cursor.execute("""
        SELECT exercise_id, name, primary_muscle, secondary_muscle
        FROM exercises
        WHERE name LIKE ?
        ORDER BY name ASC, exercise_id ASC
        LIMIT ? OFFSET ?
        """,(ex_name,limit,offset))

    else:
        cursor.execute("""
        SELECT exercise_id, name, primary_muscle, secondary_muscle
        FROM exercises
        ORDER BY name ASC, exercise_id ASC
        LIMIT ? OFFSET ?     
        """,(limit,offset))

    ex_rows = cursor.fetchall()
    conn.close()

    return [dict(x) for x in ex_rows]

@router.get("/{exercise_id}", response_model= ExerciseSummaryResponse)
def get_exercise(exercise_id:int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT exercise_id,name, primary_muscle, secondary_muscle
    FROM exercises
    WHERE exercise_id = ? 
    """,(exercise_id,))

    ex_row = cursor.fetchone()
    conn.close()

    if not ex_row:
        raise HTTPException(
            status_code = 404,
            detail= "Exercise not found for this id."        
        )
    return dict(ex_row)
        

      
    