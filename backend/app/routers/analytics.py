from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.interview import InterviewSession, InterviewStatus
from app.models.retention import RetentionReview
from app.models.skill import Skill, UserSkill
from app.models.submission import Submission
from app.models.system_design import SystemDesignAttempt
from app.models.user import User
from app.schemas.analytics import DashboardOut, DimensionScore, HabitProfileOut
from app.services.analytics.streak import compute_streak
from app.services.coach.habit_profiler import get_habit_profile

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=DashboardOut)
def dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    submissions = db.query(Submission).filter(Submission.user_id == current_user.id).all()
    sd_attempts = db.query(SystemDesignAttempt).filter(SystemDesignAttempt.user_id == current_user.id).all()
    completed_interviews = db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id, InterviewSession.status == InterviewStatus.completed
    ).all()

    def dim(values: list[float], label: str) -> DimensionScore:
        if not values:
            return DimensionScore(label=label, score=None, evidence_count=0)
        return DimensionScore(label=label, score=round(sum(values) / len(values), 3), evidence_count=len(values))

    dsa_mastery = dim([us.mastery for us in user_skills if us.attempts > 0], "DSA Mastery")
    pattern_recognition = dim(
        [us.pattern_recognition_correct / us.pattern_recognition_attempts
         for us in user_skills if us.pattern_recognition_attempts > 0],
        "Pattern Recognition",
    )
    transfer = dim(
        [us.transfer_correct / us.transfer_attempts for us in user_skills if us.transfer_attempts > 0],
        "Transfer",
    )
    now = datetime.utcnow()
    reviews = db.query(RetentionReview).filter(RetentionReview.user_id == current_user.id).all()
    retention = dim(
        [0.0 if r.due_at <= now and r.repetitions == 0 else 1.0 for r in reviews] if reviews else [],
        "Retention",
    )
    coding = dim(
        [1.0 if s.status.value == "PASSED" else 0.0 for s in submissions],
        "Coding",
    )
    from app.models.interview import InterviewMessage
    from app.services.interview.simulator import stages_for

    coverages = []
    for s in completed_interviews:
        total = len(stages_for(s.type.value)) - 1
        if total == 0:
            continue
        candidate_stages = {
            m.stage for m in db.query(InterviewMessage).filter(
                InterviewMessage.session_id == s.id, InterviewMessage.role == "candidate"
            ).all()
        }
        coverages.append(len(candidate_stages) / total)
    communication = dim(coverages, "Communication")
    system_design = dim([a.score for a in sd_attempts], "System Design")

    dims = {
        "dsa_mastery": dsa_mastery, "pattern_recognition": pattern_recognition, "transfer": transfer,
        "retention": retention, "coding": coding, "communication": communication, "system_design": system_design,
    }
    known = [d.score for d in dims.values() if d.score is not None]
    overall = round(sum(known) / len(known), 3) if known else None

    weakest = sorted(
        [
            {"skill_key": (db.query(Skill).filter(Skill.id == us.skill_id).first().key
                           if db.query(Skill).filter(Skill.id == us.skill_id).first() else "unknown"),
             "mastery": us.mastery}
            for us in user_skills if us.attempts > 0
        ],
        key=lambda x: x["mastery"],
    )[:5]

    retention_due = db.query(RetentionReview).filter(
        RetentionReview.user_id == current_user.id, RetentionReview.due_at <= now
    ).count()

    streak_days, active_days_last_30 = compute_streak(db, current_user.id)

    return DashboardOut(
        interview_readiness=dims, overall_readiness=overall, weakest_skills=weakest,
        retention_due_count=retention_due, total_submissions=len(submissions),
        total_solved=len({s.problem_id for s in submissions if s.status.value == "PASSED"}),
        current_streak_days=streak_days, active_days_last_30=active_days_last_30,
    )


@router.get("/habit-profile", response_model=HabitProfileOut)
def habit_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """A real trained neural network's read on the student's problem-solving
    HABITS -- computed from this specific user's real submission/hint/
    reasoning history, not a single problem's diagnosis. See
    services/coach/habit_profiler.py for the model and honesty notes."""
    return HabitProfileOut(**get_habit_profile(db, current_user.id))
