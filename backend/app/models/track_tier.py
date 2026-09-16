from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, JSON, String

from app.database import Base
from app.models.user import gen_id

TRACKS = ["dsa", "system_design"]


class UserTrackTier(Base):
    """Per-user tier (Novice -> Practitioner -> Expert) for an entire track
    (all of DSA, or all of System Design) -- deliberately coarser than any
    single skill's mastery. A learner earns this only by passing a real,
    dedicated assessment spanning multiple skills/cases in the track (see
    services/skill_graph/track_tier.py), never by an automatic mastery
    threshold crossing on any one topic."""

    __tablename__ = "user_track_tiers"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    track = Column(String, nullable=False)  # "dsa" | "system_design"
    tier = Column(String, default="novice")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TrackTierAssessment(Base):
    """One real attempt at advancing a track's tier. `item_ids` are frozen at
    start (a mix of problem ids, system-design case ids, and quiz question
    ids depending on the track) -- checking pass/fail always re-reads real
    Submission/ReasoningAttempt/SystemDesignAttempt/QuizAttempt rows created
    after `created_at`, never invented. The final result is an aggregate
    score across every item (see PASS_CUTOFF in track_tier.py), not a
    require-every-item-perfect bar."""

    __tablename__ = "track_tier_assessments"

    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    track = Column(String, nullable=False)
    target_tier = Column(String, nullable=False)
    item_ids = Column(JSON, default=list)  # [{"kind": "problem"|"quiz"|"case", "id": "..."}]
    status = Column(String, default="in_progress")  # "in_progress" | "passed" | "failed"
    results = Column(JSON, default=list)
    aggregate_score = Column(Float, nullable=True)  # 0..1, filled in once every item has at least one attempt
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
