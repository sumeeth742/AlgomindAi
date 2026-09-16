"""
Shared request/response shapes for the two lesson-level coaching features
(ask-anything doubt-clearing chat, and "explain it back" quality scoring),
reused identically across skills.py, system_design.py, and networks.py since
all three lesson types reduce to the same shape (a title + a markdown body).
"""
from pydantic import BaseModel


class AskLessonRequest(BaseModel):
    question: str


class AskLessonResponse(BaseModel):
    answer: str


class ExplainBackRequest(BaseModel):
    explanation: str


class ExplainBackResponse(BaseModel):
    quality_tier: str
    coaching_tip: str
    confidence: float
    matched_terms: list[str]
