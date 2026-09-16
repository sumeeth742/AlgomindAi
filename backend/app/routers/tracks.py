from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.quiz import QuizAttempt, QuizQuestion
from app.models.track_tier import TrackTierAssessment
from app.models.user import User
from app.schemas.track import (
    QuizAnswerRequest, QuizAnswerResponse, TrackAssessmentCheckItem, TrackAssessmentCheckOut,
    TrackAssessmentItemOut, TrackAssessmentStartOut, TrackTierStatusOut,
)
from app.services.skill_graph.track_tier import (
    TRACKS, check_track_assessment, get_track_status, resolve_track_assessment, start_track_assessment,
)

router = APIRouter(prefix="/tracks", tags=["tracks"])


def _validate_track(track: str):
    if track not in TRACKS:
        raise HTTPException(status_code=404, detail="Unknown track")


@router.get("/{track}/tier-status", response_model=TrackTierStatusOut)
def tier_status(track: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _validate_track(track)
    status = get_track_status(db, current_user.id, track)
    return TrackTierStatusOut(
        track=track, current_tier=status.current_tier, next_tier=status.next_tier,
        detail=status.detail, active_assessment_id=status.active_assessment_id,
    )


@router.post("/{track}/tier-assessment/start", response_model=TrackAssessmentStartOut)
def start_tier_assessment(track: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _validate_track(track)
    result = start_track_assessment(db, current_user.id, track)
    if not result.ok:
        db.rollback()
        return TrackAssessmentStartOut(ok=False, reason=result.reason)
    db.commit()
    return TrackAssessmentStartOut(
        ok=True, assessment_id=result.assessment.id, target_tier=result.assessment.target_tier,
        items=[TrackAssessmentItemOut(kind=i.kind, slug=i.slug, title=i.title, options=i.options) for i in result.items],
    )


@router.post("/{track}/tier-assessment/{assessment_id}/quiz-answer", response_model=QuizAnswerResponse)
def answer_quiz_question(
    track: str, assessment_id: str, payload: QuizAnswerRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    _validate_track(track)
    assessment = db.query(TrackTierAssessment).filter(
        TrackTierAssessment.id == assessment_id, TrackTierAssessment.user_id == current_user.id, TrackTierAssessment.track == track,
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if assessment.status != "in_progress":
        raise HTTPException(status_code=400, detail="This assessment is already resolved.")
    if not any(i["kind"] == "quiz" and i["id"] == payload.question_id for i in assessment.item_ids):
        raise HTTPException(status_code=400, detail="This question isn't part of this assessment.")

    question = db.query(QuizQuestion).filter(QuizQuestion.id == payload.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = payload.selected_index == question.correct_index
    db.add(QuizAttempt(
        user_id=current_user.id, question_id=question.id,
        selected_index=payload.selected_index, is_correct=is_correct,
    ))
    db.commit()
    return QuizAnswerResponse(correct=is_correct, correct_index=question.correct_index, explanation=question.explanation)


@router.post("/{track}/tier-assessment/{assessment_id}/check", response_model=TrackAssessmentCheckOut)
def check_tier_assessment(
    track: str, assessment_id: str,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    _validate_track(track)
    assessment = db.query(TrackTierAssessment).filter(
        TrackTierAssessment.id == assessment_id, TrackTierAssessment.user_id == current_user.id, TrackTierAssessment.track == track,
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if assessment.status != "in_progress":
        return TrackAssessmentCheckOut(
            status=assessment.status, target_tier=assessment.target_tier, aggregate_score=assessment.aggregate_score,
            checks=[
                TrackAssessmentCheckItem(
                    kind=r["kind"], slug=r["slug"], title=r["title"], score=r["score"], passed=r["passed"],
                    reason=r["reason"], options=r.get("options"),
                )
                for r in (assessment.results or [])
            ],
        )

    result = check_track_assessment(db, assessment)
    resolve_track_assessment(db, assessment, result)
    db.commit()
    return TrackAssessmentCheckOut(
        status=result.status, target_tier=assessment.target_tier, aggregate_score=result.aggregate_score,
        checks=[
            TrackAssessmentCheckItem(kind=c.kind, slug=c.slug, title=c.title, score=c.score, passed=c.passed, reason=c.reason, options=c.options)
            for c in result.checks
        ],
    )
