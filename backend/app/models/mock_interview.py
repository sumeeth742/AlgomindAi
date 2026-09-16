from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, JSON, String, Text

from app.database import Base
from app.models.user import gen_id


class MockInterviewLoop(Base):
    """A single timed, three-round mock "onsite" -- one DSA problem, one
    System Design case, one behavioral question -- chained into one session
    with one combined report at the end, instead of practicing each in
    isolation. Deliberately does NOT reimplement DSA/System Design grading:
    each round links to a real Submission / SystemDesignAttempt row created
    through the app's own already-verified /problems/submit and
    /system-design/cases/attempt endpoints, so "verification" here means
    "point at the real graded record," never a second, parallel judgment
    that could disagree with the first. Only the behavioral round needed new
    verification logic, since nothing existed for it yet -- see
    services/interview/behavioral.py for the real, structural (not invented)
    STAR-format check."""

    __tablename__ = "mock_interview_loops"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    stage = Column(String, default="dsa")  # dsa -> system_design -> behavioral -> completed

    dsa_problem_id = Column(String, ForeignKey("problems.id"), nullable=False)
    dsa_submission_id = Column(String, ForeignKey("submissions.id"), nullable=True)

    sd_case_id = Column(String, ForeignKey("system_design_cases.id"), nullable=False)
    sd_attempt_id = Column(String, ForeignKey("system_design_attempts.id"), nullable=True)

    behavioral_question = Column(Text, nullable=False)
    behavioral_answer = Column(Text, default="")
    behavioral_score = Column(Float, nullable=True)
    behavioral_matched_parts = Column(JSON, default=list)

    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
