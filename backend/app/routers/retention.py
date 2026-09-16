from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.retention import LearningEvent, ReviewResult, RetentionReview
from app.models.skill import Skill
from app.models.user import User
from app.schemas.retention import DueReviewOut, SubmitReviewRequest, SubmitReviewResponse
from app.services.retention.scheduler import apply_review

router = APIRouter(prefix="/retention", tags=["retention"])


@router.get("/due", response_model=list[DueReviewOut])
def due_reviews(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.utcnow()
    rows = (
        db.query(RetentionReview)
        .filter(RetentionReview.user_id == current_user.id, RetentionReview.due_at <= now)
        .order_by(RetentionReview.due_at.asc())
        .all()
    )
    out = []
    for r in rows:
        skill = db.query(Skill).filter(Skill.id == r.skill_id).first()
        if not skill:
            continue
        out.append(DueReviewOut(
            review_id=r.id, skill_key=skill.key, skill_name=skill.name,
            due_at=r.due_at.isoformat(), interval_days=r.interval_days, repetitions=r.repetitions,
        ))
    return out


@router.post("/{review_id}/submit", response_model=SubmitReviewResponse)
def submit_review(
    review_id: str, payload: SubmitReviewRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    review = db.query(RetentionReview).filter(
        RetentionReview.id == review_id, RetentionReview.user_id == current_user.id
    ).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    try:
        result = ReviewResult(payload.result)
    except ValueError:
        raise HTTPException(status_code=400, detail="result must be one of again|hard|good|easy")

    apply_review(review, result)
    db.add(LearningEvent(
        user_id=current_user.id, event_type="RETENTION_REVIEW", skill_id=review.skill_id,
        payload={"result": payload.result},
    ))
    db.commit()
    return SubmitReviewResponse(
        next_due_at=review.due_at.isoformat(), interval_days=review.interval_days, ease_factor=review.ease_factor,
    )
