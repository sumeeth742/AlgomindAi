import enum
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum, Float

from app.database import Base
from app.models.user import gen_id


class ActivityType(str, enum.Enum):
    lesson = "LESSON"
    recall = "RECALL"
    pattern_drill = "PATTERN_DRILL"
    easy_problem = "EASY_PROBLEM"
    medium_problem = "MEDIUM_PROBLEM"
    hard_problem = "HARD_PROBLEM"
    debugging = "DEBUGGING"
    optimization = "OPTIMIZATION"
    transfer = "TRANSFER"
    retention_review = "RETENTION_REVIEW"
    system_design_lesson = "SYSTEM_DESIGN_LESSON"
    hld_case = "HLD_CASE"
    mock_interview = "MOCK_INTERVIEW"
    contest = "CONTEST"


class RecommendationStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    dismissed = "dismissed"


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    activity_type = Column(Enum(ActivityType), nullable=False)
    skill_id = Column(String, ForeignKey("skills.id"), nullable=True)
    problem_id = Column(String, ForeignKey("problems.id"), nullable=True)

    reason_what = Column(Text, nullable=False)
    reason_why = Column(Text, nullable=False)
    expected_outcome = Column(Text, nullable=False)
    priority_score = Column(Float, default=0.0)

    status = Column(Enum(RecommendationStatus), default=RecommendationStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
