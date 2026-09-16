from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import gen_id


class Skill(Base):
    """A node in the skill graph, e.g. ARRAYS_TRAVERSAL, SLIDING_WINDOW."""

    __tablename__ = "skills"

    id = Column(String, primary_key=True, default=gen_id)
    key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    chapter = Column(String, nullable=False)  # e.g. "Arrays"
    level = Column(Integer, default=1)  # 0-4, matches curriculum levels
    description = Column(Text, default="")
    concept_markdown = Column(Text, default="")  # full lesson content
    mnemonic = Column(Text, default="")  # a short, memorable hook for fast recall -- shown before the full lesson
    # A plain-language walkthrough of the same concept as a short back-and-forth
    # dialogue (list of {"speaker": "mira"|"dev", "text": ...}), rendered as a
    # comic strip -- a jargon-light second path through the material for anyone
    # who bounces off the dense lesson prose, not a replacement for it.
    comic_script = Column(JSON, default=list)

    prerequisites = relationship(
        "SkillPrerequisite",
        foreign_keys="SkillPrerequisite.skill_id",
        back_populates="skill",
        cascade="all, delete-orphan",
    )


class SkillPrerequisite(Base):
    __tablename__ = "skill_prerequisites"

    id = Column(String, primary_key=True, default=gen_id)
    skill_id = Column(String, ForeignKey("skills.id"), nullable=False)
    prerequisite_skill_id = Column(String, ForeignKey("skills.id"), nullable=False)

    skill = relationship("Skill", foreign_keys=[skill_id], back_populates="prerequisites")
    prerequisite_skill = relationship("Skill", foreign_keys=[prerequisite_skill_id])


class UserSkill(Base):
    """Per-user mastery state for a single skill node (the granular skill graph)."""

    __tablename__ = "user_skills"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    skill_id = Column(String, ForeignKey("skills.id"), nullable=False)

    # Mastery is purely informational progress on this one skill ("how much
    # have they learnt here") -- it is not tiered per-skill. Tiers
    # (Novice/Practitioner/Expert) live one level up, on the whole DSA or
    # System Design track (see models/track_tier.py + skill_graph/track_tier.py),
    # and only advance through a real, dedicated cross-skill assessment.
    mastery = Column(Float, default=0.0)  # 0..1, EWMA of correctness weighted by difficulty
    confidence = Column(Float, default=0.0)  # 0..1, inverse of variance/evidence sparsity
    attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    pattern_recognition_attempts = Column(Integer, default=0)
    pattern_recognition_correct = Column(Integer, default=0)
    transfer_attempts = Column(Integer, default=0)
    transfer_correct = Column(Integer, default=0)
    last_practiced_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="user_skills")
    skill = relationship("Skill")
