from pydantic import BaseModel


class TrackTierStatusOut(BaseModel):
    track: str
    current_tier: str
    next_tier: str | None
    detail: str
    active_assessment_id: str | None


class TrackAssessmentItemOut(BaseModel):
    kind: str  # "problem" | "quiz" | "case"
    slug: str
    title: str
    options: list[str] | None = None


class TrackAssessmentStartOut(BaseModel):
    ok: bool
    reason: str | None = None
    assessment_id: str | None = None
    target_tier: str | None = None
    items: list[TrackAssessmentItemOut] = []


class QuizAnswerRequest(BaseModel):
    question_id: str
    selected_index: int


class QuizAnswerResponse(BaseModel):
    correct: bool
    correct_index: int
    explanation: str


class TrackAssessmentCheckItem(BaseModel):
    kind: str
    slug: str
    title: str
    score: float
    passed: bool
    reason: str
    options: list[str] | None = None


class TrackAssessmentCheckOut(BaseModel):
    status: str
    target_tier: str
    aggregate_score: float | None
    checks: list[TrackAssessmentCheckItem]
