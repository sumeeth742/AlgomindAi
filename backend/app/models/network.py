from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text

from app.database import Base
from app.models.user import gen_id


class NetworkLesson(Base):
    """Computer Networks curriculum -- a genuinely separate feature from
    System Design (its own nav item, its own content), not folded into
    System Design's Foundations track, per explicit user direction. Mirrors
    SystemDesignLesson's proven shape (slug/level/category/content) so it can
    reuse the same Markdown/LessonActs/ConceptMapStrip frontend components
    and the same level+category-adjacency concept-map pattern."""

    __tablename__ = "network_lessons"

    id = Column(String, primary_key=True, default=gen_id)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    level = Column(Integer, default=0)
    category = Column(String, default="")  # e.g. "fundamentals", "transport", "security"
    content_markdown = Column(Text, nullable=False)
    practical_connection = Column(Text, default="")  # how this shows up in real backend/systems work
    # Same jargon-light comic-strip walkthrough as Skill.comic_script -- see
    # that field's docstring for the format and intent.
    comic_script = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class NetworkQuizQuestion(Base):
    """A real, deterministically-graded multiple-choice question attached to
    one Networks lesson -- the practice/assessment layer this curriculum
    otherwise lacks (no coding problems the way DSA has, no case studies the
    way System Design has). Grading is exact correct-option matching."""

    __tablename__ = "network_quiz_questions"

    id = Column(String, primary_key=True, default=gen_id)
    lesson_id = Column(String, ForeignKey("network_lessons.id"), nullable=False)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # list[str]
    correct_index = Column(Integer, nullable=False)
    explanation = Column(Text, default="")


class NetworkQuizAttempt(Base):
    __tablename__ = "network_quiz_attempts"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    question_id = Column(String, ForeignKey("network_quiz_questions.id"), nullable=False)
    selected_index = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
