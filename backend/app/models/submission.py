import enum
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON, Enum, Boolean
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import gen_id


class SubmissionStatus(str, enum.Enum):
    passed = "PASSED"
    failed = "FAILED"
    timeout = "TIMEOUT"
    runtime_error = "RUNTIME_ERROR"
    compile_error = "COMPILE_ERROR"
    memory_limit = "MEMORY_LIMIT"


class SubmissionMode(str, enum.Enum):
    guided = "guided"
    standard = "standard"
    blind = "blind"
    pattern_recognition = "pattern_recognition"
    debugging = "debugging"
    optimization = "optimization"
    complexity = "complexity"
    transfer = "transfer"
    interview = "interview"
    contest = "contest"


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    problem_id = Column(String, ForeignKey("problems.id"), nullable=False)
    mode = Column(Enum(SubmissionMode), default=SubmissionMode.standard)
    language = Column(String, default="python")
    code = Column(Text, nullable=False)

    status = Column(Enum(SubmissionStatus), nullable=False)
    passed_count = Column(Integer, default=0)
    total_count = Column(Integer, default=0)
    runtime_ms = Column(Float, default=0.0)
    peak_memory_kb = Column(Float, nullable=True)
    test_results = Column(JSON, default=list)  # per-test PASS/FAIL detail, hidden results redacted for client
    error_message = Column(Text, nullable=True)
    diagnosis = Column(JSON, nullable=True)  # {primary_issue, confidence, evidence, recommendation} from the diagnosis engine

    hint_count_used = Column(Integer, default=0)
    time_to_solve_seconds = Column(Float, nullable=True)
    attempt_number = Column(Integer, default=1)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem")


class ReasoningAttempt(Base):
    """Pattern-recognition mode: student declares a pattern + justification before coding."""

    __tablename__ = "reasoning_attempts"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    problem_id = Column(String, ForeignKey("problems.id"), nullable=False)
    declared_pattern = Column(String, nullable=False)
    reasoning_text = Column(Text, default="")
    is_correct_pattern = Column(Boolean, nullable=False)
    reasoning_quality_score = Column(Float, default=0.0)  # 0..1, keyword/evidence overlap based
    evidence_matched = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
