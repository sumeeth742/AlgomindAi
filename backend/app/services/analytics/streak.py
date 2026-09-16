"""Study streak, computed from real LearningEvent timestamps -- never estimated."""
from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.retention import LearningEvent


def compute_streak(db: Session, user_id: str) -> tuple[int, int]:
    """Returns (current_streak_days, active_days_last_30). A day counts as
    active if the user has at least one LearningEvent on it. The current streak
    counts consecutive active days ending today or yesterday -- a gap of two or
    more days breaks it, but a streak isn't lost just because today hasn't
    happened yet."""
    events = db.query(LearningEvent.created_at).filter(LearningEvent.user_id == user_id).all()
    active_dates = {e[0].date() for e in events}
    if not active_dates:
        return 0, 0

    today = date.today()
    active_days_last_30 = sum(1 for d in active_dates if (today - d).days < 30)

    streak = 0
    cursor = today
    if cursor not in active_dates:
        cursor -= timedelta(days=1)  # today not active yet is fine, check from yesterday
    while cursor in active_dates:
        streak += 1
        cursor -= timedelta(days=1)

    return streak, active_days_last_30
