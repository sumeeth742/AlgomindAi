import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship

from app.database import Base


def gen_id() -> str:
    return uuid.uuid4().hex


class InterfaceMode(str, enum.Enum):
    beginner = "beginner"
    expert = "expert"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_id)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    interface_mode = Column(Enum(InterfaceMode), default=InterfaceMode.beginner)
    target_track = Column(String, nullable=True)  # e.g. "faang-style", "startup"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
