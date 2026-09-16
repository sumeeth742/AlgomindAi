import enum
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum, JSON

from app.database import Base
from app.models.user import gen_id


class InterviewType(str, enum.Enum):
    dsa = "dsa"
    system_design = "system_design"


class InterviewStatus(str, enum.Enum):
    active = "active"
    completed = "completed"


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(InterviewType), nullable=False)
    problem_id = Column(String, ForeignKey("problems.id"), nullable=True)
    case_id = Column(String, ForeignKey("system_design_cases.id"), nullable=True)
    status = Column(Enum(InterviewStatus), default=InterviewStatus.active)
    stage = Column(String, default="clarify")  # tracks the interview stage machine, see services/interview
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    final_report = Column(JSON, nullable=True)


class InterviewMessage(Base):
    __tablename__ = "interview_messages"

    id = Column(String, primary_key=True, default=gen_id)
    session_id = Column(String, ForeignKey("interview_sessions.id"), nullable=False)
    role = Column(String, nullable=False)  # "interviewer" | "candidate"
    stage = Column(String, default="")
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
