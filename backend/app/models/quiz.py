from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import gen_id


class QuizQuestion(Base):
    """A real, deterministically-graded multiple-choice question for a
    theory-only skill -- one with no coding problems to build practical
    mastery against (e.g. Algorithmic Thinking & Complexity has zero seeded
    problems; Programming Foundations is graded here rather than via mastery
    too, since the user considers it foundational/conceptual). Grading is
    exact correct-option matching, never an LLM judgment call. Mastery on
    these skills is still tracked and shown (how much the learner has
    engaged with the lesson/problems), but it does not gate DSA track
    eligibility the way it does for every other skill -- these questions do."""

    __tablename__ = "quiz_questions"

    id = Column(String, primary_key=True, default=gen_id)
    skill_id = Column(String, ForeignKey("skills.id"), nullable=False)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # list[str]
    correct_index = Column(Integer, nullable=False)
    explanation = Column(Text, default="")

    skill = relationship("Skill")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    question_id = Column(String, ForeignKey("quiz_questions.id"), nullable=False)
    selected_index = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
