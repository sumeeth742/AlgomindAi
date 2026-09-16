import enum
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum, JSON

from app.database import Base
from app.models.user import gen_id


class ReviewResult(str, enum.Enum):
    again = "again"       # failed recall entirely
    hard = "hard"
    good = "good"
    easy = "easy"


class RetentionReview(Base):
    """One skill's spaced-repetition state for one user, scheduled via SM-2."""

    __tablename__ = "retention_reviews"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    skill_id = Column(String, ForeignKey("skills.id"), nullable=False)

    ease_factor = Column(Float, default=2.5)
    interval_days = Column(Float, default=1.0)
    repetitions = Column(Integer, default=0)
    due_at = Column(DateTime, default=datetime.utcnow)
    last_reviewed_at = Column(DateTime, nullable=True)
    last_result = Column(Enum(ReviewResult), nullable=True)


class LearningEvent(Base):
    """Append-only log of everything the learner does; source of truth for analytics/diagnosis."""

    __tablename__ = "learning_events"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    event_type = Column(String, nullable=False)  # e.g. SUBMISSION, HINT_USED, LESSON_VIEWED, RECALL_REVIEW
    skill_id = Column(String, ForeignKey("skills.id"), nullable=True)
    problem_id = Column(String, ForeignKey("problems.id"), nullable=True)
    payload = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
