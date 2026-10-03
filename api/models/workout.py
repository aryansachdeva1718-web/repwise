from pydantic import BaseModel


class WorkoutResponse(BaseModel):
    session_id: int
    title: str
    start_time: str
    end_time: str | None = None
    description: str | None = None