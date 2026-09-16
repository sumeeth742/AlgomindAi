from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Float

from app.database import Base
from app.models.user import gen_id


class Contest(Base):
    __tablename__ = "contests"

    id = Column(String, primary_key=True, default=gen_id)
    title = Column(String, nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    problem_ids = Column(JSON, default=list)


class ContestSubmission(Base):
    __tablename__ = "contest_submissions"

    id = Column(String, primary_key=True, default=gen_id)
    contest_id = Column(String, ForeignKey("contests.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    problem_id = Column(String, ForeignKey("problems.id"), nullable=False)
    submission_id = Column(String, ForeignKey("submissions.id"), nullable=False)
    score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
