from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON

from app.database import Base
from app.models.user import gen_id


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    summary = Column(JSON, default=dict)  # {strong: [...], weak: [...], recurring_errors: [...], next: [...]}
