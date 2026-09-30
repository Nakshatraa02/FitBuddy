from pydantic import BaseModel, Field


class UserInput(BaseModel):
    username: str
    user_id: str
    age: int = Field(gt=0, lt=120)
    weight: float = Field(gt=0)
    goal: str
    intensity: str


class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str