from pydantic import BaseModel


class RecommendationOut(BaseModel):
    id: str
    activity_type: str
    skill_key: str | None
    problem_slug: str | None
    reason_what: str
    reason_why: str
    expected_outcome: str
