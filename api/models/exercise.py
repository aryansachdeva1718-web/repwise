from pydantic import BaseModel

class ExerciseSummaryResponse(BaseModel):
    exercise_id: int
    name: str
    primary_muscle: str | None = None
    secondary_muscle: str | None = None