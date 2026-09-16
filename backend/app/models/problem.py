import enum
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON, Enum, Boolean
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import gen_id


class Difficulty(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
    expert = "expert"


class Problem(Base):
    __tablename__ = "problems"

    id = Column(String, primary_key=True, default=gen_id)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    statement_markdown = Column(Text, nullable=False)
    difficulty = Column(Enum(Difficulty), nullable=False)

    # multi-dimensional difficulty per spec section 30
    concept_difficulty = Column(Integer, default=1)  # 1-5
    implementation_difficulty = Column(Integer, default=1)
    reasoning_difficulty = Column(Integer, default=1)
    pattern_difficulty = Column(Integer, default=1)

    primary_skill_id = Column(String, ForeignKey("skills.id"), nullable=False)
    pattern_skill_ids = Column(JSON, default=list)  # list of Skill.key candidate patterns

    constraints_markdown = Column(Text, default="")
    examples = Column(JSON, default=list)  # [{input, output, explanation}]

    function_name = Column(String, nullable=False)
    # Optional per-argument / result conversions applied by the sandbox before/after
    # calling the user's function, e.g. {"args": {"0": "linked_list"}, "result": "linked_list"}
    # -- lets problems exchange linked-list/tree structures over JSON-only test data.
    io_transform = Column(JSON, default=dict)
    # "exact" (default) requires the output to match expected_output exactly.
    # "unordered_nested" is for problems like subsets/permutations where many
    # correct enumeration orders exist -- both sides are sorted before comparing
    # so a correct solution isn't marked wrong just for using a different valid order.
    output_comparison = Column(String, default="exact")
    starter_code_python = Column(Text, nullable=False)
    reference_solution_python = Column(Text, nullable=True)  # for editorial/validation only, never sent to client

    time_limit_ms = Column(Integer, default=2000)
    memory_limit_mb = Column(Integer, default=256)
    expected_complexity = Column(String, default="")  # e.g. "O(n)"

    is_transfer_variant_of = Column(String, ForeignKey("problems.id"), nullable=True)
    variant_description = Column(Text, default="")

    editorial_markdown = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    primary_skill = relationship("Skill")
    test_cases = relationship("ProblemTestCase", back_populates="problem", cascade="all, delete-orphan")
    hints = relationship("Hint", back_populates="problem", cascade="all, delete-orphan")


class ProblemTestCase(Base):
    __tablename__ = "problem_test_cases"

    id = Column(String, primary_key=True, default=gen_id)
    problem_id = Column(String, ForeignKey("problems.id"), nullable=False)
    args = Column(JSON, nullable=False)  # list of positional args to pass to function
    expected_output = Column(JSON, nullable=False)
    is_hidden = Column(Boolean, default=False)
    explanation = Column(Text, default="")

    problem = relationship("Problem", back_populates="test_cases")


class Hint(Base):
    __tablename__ = "hints"

    id = Column(String, primary_key=True, default=gen_id)
    problem_id = Column(String, ForeignKey("problems.id"), nullable=False)
    level = Column(Integer, nullable=False)  # 1..5, per section 53
    text_markdown = Column(Text, nullable=False)

    problem = relationship("Problem", back_populates="hints")


class HintUsage(Base):
    __tablename__ = "hint_usages"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    problem_id = Column(String, ForeignKey("problems.id"), nullable=False)
    hint_id = Column(String, ForeignKey("hints.id"), nullable=False)
    used_at = Column(DateTime, default=datetime.utcnow)
