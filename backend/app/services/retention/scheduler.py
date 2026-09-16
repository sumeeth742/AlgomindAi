"""
SM-2 spaced-repetition scheduling (the classic Anki/SuperMemo algorithm),
applied to skills instead of flashcards. See spec section 51: Day 1/3/7/14/30/60
is exactly the interval sequence SM-2 converges to for consistently "good" recall.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from app.models.retention import RetentionReview, ReviewResult

QUALITY_MAP = {
    ReviewResult.again: 0,
    ReviewResult.hard: 3,
    ReviewResult.good: 4,
    ReviewResult.easy: 5,
}


def apply_review(review: RetentionReview, result: ReviewResult) -> RetentionReview:
    quality = QUALITY_MAP[result]
    now = datetime.utcnow()

    if quality < 3:
        review.repetitions = 0
        review.interval_days = 1.0
    else:
        if review.repetitions == 0:
            review.interval_days = 1.0
        elif review.repetitions == 1:
            review.interval_days = 3.0
        else:
            review.interval_days = round(review.interval_days * review.ease_factor, 2)
        review.repetitions += 1

    new_ef = review.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    review.ease_factor = max(1.3, round(new_ef, 3))

    review.last_reviewed_at = now
    review.last_result = result
    review.due_at = now + timedelta(days=review.interval_days)
    return review


def get_or_create_review(db, user_id: str, skill_id: str) -> RetentionReview:
    review = (
        db.query(RetentionReview)
        .filter(RetentionReview.user_id == user_id, RetentionReview.skill_id == skill_id)
        .first()
    )
    if review is None:
        review = RetentionReview(user_id=user_id, skill_id=skill_id)
        db.add(review)
        db.flush()
    return review
