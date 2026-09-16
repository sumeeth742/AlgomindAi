from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.problem import Problem
from app.models.recommendation import Recommendation
from app.models.skill import Skill
from app.models.user import User
from app.schemas.recommendation import RecommendationOut
from app.services.recommendation.engine import build_recommendations

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=list[RecommendationOut])
def get_recommendations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raw = build_recommendations(db, current_user.id)
    out = []
    for r in raw:
        rec = Recommendation(
            user_id=current_user.id, activity_type=r["activity_type"], skill_id=r["skill_id"],
            problem_id=r["problem_id"], reason_what=r["reason_what"], reason_why=r["reason_why"],
            expected_outcome=r["expected_outcome"], priority_score=r["priority_score"],
        )
        db.add(rec)
        db.flush()  # populate rec.id (the default is applied on flush, not on construction)
        skill = db.query(Skill).filter(Skill.id == r["skill_id"]).first() if r["skill_id"] else None
        problem = db.query(Problem).filter(Problem.id == r["problem_id"]).first() if r["problem_id"] else None
        out.append(RecommendationOut(
            id=rec.id, activity_type=r["activity_type"], skill_key=skill.key if skill else None,
            problem_slug=problem.slug if problem else None, reason_what=r["reason_what"],
            reason_why=r["reason_why"], expected_outcome=r["expected_outcome"],
        ))
    db.commit()
    return out
