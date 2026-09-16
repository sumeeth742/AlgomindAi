from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON, Float

from app.database import Base
from app.models.user import gen_id


class SystemDesignLesson(Base):
    __tablename__ = "system_design_lessons"

    id = Column(String, primary_key=True, default=gen_id)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    level = Column(Integer, default=0)  # 0-8 per curriculum levels in spec sections 36-44
    category = Column(String, default="")  # e.g. "foundations", "caching", "microservices"
    content_markdown = Column(Text, nullable=False)
    dsa_connection = Column(Text, default="")  # explicit DSA <-> system design link, section 49
    # Same jargon-light comic-strip walkthrough as Skill.comic_script -- see
    # that field's docstring for the format and intent.
    comic_script = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class SystemDesignCase(Base):
    __tablename__ = "system_design_cases"

    id = Column(String, primary_key=True, default=gen_id)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    difficulty = Column(String, default="intermediate")
    description_markdown = Column(Text, nullable=False)
    functional_requirements = Column(JSON, default=list)
    non_functional_requirements = Column(JSON, default=list)
    estimation_prompt = Column(Text, default="")  # e.g. "10M users, 10 req/day..."
    estimation_expected = Column(JSON, default=dict)  # {qps: ..., storage_gb_per_day: ...} with tolerance
    expected_components = Column(JSON, default=list)  # components a good design should include, for critique engine
    editorial_markdown = Column(Text, default="")

    # Same underlying case, deliberately different scale: e.g. "url-shortener"
    # groups "url-shortener-startup" / "-growth" / "-global", each a genuinely
    # different set of expected_components (not just bigger numbers on the same
    # architecture) since the whole point is that the *right answer* changes
    # with scale -- see system_design_seed.py.
    base_slug = Column(String, index=True, nullable=True)
    scale_tier = Column(String, nullable=True)  # "startup" | "growth" | "global"
    scale_description = Column(Text, default="")  # one-line scale assumption shown next to the tier picker


class SystemDesignAttempt(Base):
    __tablename__ = "system_design_attempts"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    case_id = Column(String, ForeignKey("system_design_cases.id"), nullable=False)
    architecture = Column(JSON, default=dict)  # {nodes: [...], edges: [...]}
    estimation_answers = Column(JSON, default=dict)
    feedback = Column(JSON, default=dict)  # rule-based critique: missing components, unjustified components, etc.
    score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class LLDCase(Base):
    """A practical low-level design exercise -- 'design a parking lot,' 'design
    an elevator system' -- graded the same rule-based way as the HLD case
    studies above (missing/unjustified + why-questions), just applied to
    classes and their relationships instead of infrastructure components."""

    __tablename__ = "lld_cases"

    id = Column(String, primary_key=True, default=gen_id)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    difficulty = Column(String, default="intermediate")
    description_markdown = Column(Text, nullable=False)
    functional_requirements = Column(JSON, default=list)
    non_functional_requirements = Column(JSON, default=list)
    # [{"name": str, "aliases": [str, ...], "responsibility": str}, ...] -- the
    # core classes a reasonable design should include, matched by name/alias,
    # never penalizing a learner for a synonym they reasonably chose.
    expected_classes = Column(JSON, default=list)
    abstraction_hint = Column(Text, default="")  # e.g. "vehicle types should share a common parent/interface"
    editorial_markdown = Column(Text, default="")


class LLDAttempt(Base):
    __tablename__ = "lld_attempts"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    case_id = Column(String, ForeignKey("lld_cases.id"), nullable=False)
    # [{"name": str, "fields": [str], "methods": [str], "extends": str|None, "implements": [str]}, ...]
    classes = Column(JSON, default=list)
    feedback = Column(JSON, default=dict)
    score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
