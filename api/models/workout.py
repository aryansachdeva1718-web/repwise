from pydantic import BaseModel


class WorkoutSummaryResponse(BaseModel):
    session_id: int
    title: str
    start_time: str
    end_time: str | None = None
    description: str | None = None

class SetResponse(BaseModel):
    set_number: int
    set_type: str
    weight: float | None = None
    reps: int | None = None
    rpe: float | None = None


class ExerciseResponse(BaseModel):
    exercise_id: int
    name: str
    sets: list[SetResponse]

class WorkoutDetailResponse(BaseModel):
    session_id: int
    title: str
    start_time: str
    end_time: str | None = None
    description: str | None = None
    exercises : list[ExerciseResponse]