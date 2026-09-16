from datetime import datetime

from pydantic import BaseModel


class ContestProblemOut(BaseModel):
    slug: str
    title: str
    difficulty: str


class ContestOut(BaseModel):
    id: str
    title: str
    start_at: datetime
    end_at: datetime
    status: str  # "upcoming" | "live" | "ended"
    problem_count: int


class ContestDetailOut(ContestOut):
    problems: list[ContestProblemOut]  # empty while status == "upcoming" -- no peeking early


class ContestSubmitRequest(BaseModel):
    code: str
    language: str = "python"


class LeaderboardEntryOut(BaseModel):
    rank: int
    user_name: str
    total_score: float
    problems_solved: int
