from pydantic import BaseModel, Field

class SetCreate(BaseModel):
    weight: float | None = Field(default=None, ge=0)
    reps: int | None = Field(default=None, ge=0)
    set_type: str = "Normal"

class ExerciseCreate(BaseModel):
    exercise_id: int = Field(gt=0)
    sets: list[SetCreate] = Field(min_length=1)

class WorkoutCreate(BaseModel):
    title: str = Field(min_length=1)
    start_time: str
    end_time: str | None= None
    description: str | None = None
    exercises: list[ExerciseCreate] = Field(min_length=1)