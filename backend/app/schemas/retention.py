from pydantic import BaseModel


class DueReviewOut(BaseModel):
    review_id: str
    skill_key: str
    skill_name: str
    due_at: str
    interval_days: float
    repetitions: int


class SubmitReviewRequest(BaseModel):
    result: str  # again | hard | good | easy


class SubmitReviewResponse(BaseModel):
    next_due_at: str
    interval_days: float
    ease_factor: float
