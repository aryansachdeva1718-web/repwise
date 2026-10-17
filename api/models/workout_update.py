from pydantic import BaseModel, field_validator

class WorkoutUpdate(BaseModel):
    title: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    description: str | None = None

    @field_validator("title", "start_time")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value