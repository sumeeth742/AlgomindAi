from pydantic import BaseModel


class DimensionScore(BaseModel):
    label: str
    score: float | None  # None = INSUFFICIENT_EVIDENCE
    evidence_count: int


class DashboardOut(BaseModel):
    interview_readiness: dict[str, DimensionScore]
    overall_readiness: float | None
    weakest_skills: list[dict]
    retention_due_count: int
    total_submissions: int
    total_solved: int
    current_streak_days: int
    active_days_last_30: int


class HabitProfileOut(BaseModel):
    available: bool
    reason: str | None = None
    habit: str | None = None
    coaching_tip: str | None = None
    confidence: float | None = None
    features: dict | None = None
