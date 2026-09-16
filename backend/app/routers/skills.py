from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.problem import Problem
from app.models.skill import Skill, SkillPrerequisite, UserSkill
from app.models.submission import Submission
from app.models.user import User
from app.schemas.lesson_coach import AskLessonRequest, AskLessonResponse, ExplainBackRequest, ExplainBackResponse
from app.schemas.problem import TransferChallengeOut
from app.schemas.skill import ConceptMapNodeOut, ConceptMapOut, SkillLessonOut, SkillOut, SkillReadinessOut, UserSkillOut
from app.services.coach.explain_back_scorer import score_explanation
from app.services.llm.lesson_qa import LocalLLMUnavailable, ask_about_lesson
from app.services.skill_graph.graph import prerequisites_met

router = APIRouter(prefix="/skills", tags=["skills"])

TRANSFER_MASTERY_THRESHOLD = 0.6


@router.get("", response_model=list[SkillOut])
def list_skills(db: Session = Depends(get_db)):
    return db.query(Skill).order_by(Skill.level.asc(), Skill.chapter.asc()).all()


@router.get("/readiness", response_model=list[SkillReadinessOut])
def skill_readiness(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Whether the user's prerequisites are met for each skill (spec section 60: the
    recommendation engine respects prerequisites; this exposes the same check so the
    UI can visibly guide learners to start from fundamentals instead of jumping
    straight to an advanced topic they lack the grounding for. Informational only --
    skills aren't hard-blocked, since a curious learner previewing ahead is fine."""
    skills = db.query(Skill).all()
    out = []
    for skill in skills:
        ready, unmet = prerequisites_met(db, current_user.id, skill.id)
        out.append(SkillReadinessOut(skill_key=skill.key, ready=ready, unmet_prerequisites=unmet))
    return out


@router.get("/{skill_key}/lesson", response_model=SkillLessonOut)
def get_lesson(skill_key: str, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.key == skill_key).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.post("/{skill_key}/ask", response_model=AskLessonResponse)
def ask_about_skill_lesson(skill_key: str, payload: AskLessonRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.key == skill_key).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    try:
        answer = ask_about_lesson(skill.name, skill.concept_markdown, payload.question)
    except LocalLLMUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))
    return AskLessonResponse(answer=answer)


@router.post("/{skill_key}/explain-back", response_model=ExplainBackResponse)
def explain_skill_back(skill_key: str, payload: ExplainBackRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.key == skill_key).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return ExplainBackResponse(**score_explanation(skill.name, skill.concept_markdown, payload.explanation))


@router.get("/{skill_key}/concept-map", response_model=ConceptMapOut)
def get_concept_map(skill_key: str, db: Session = Depends(get_db)):
    """Orientation graphic data for a lesson: real prerequisite skills (what you
    need before this) and real 'unlocks' (skills that list this one as a
    prerequisite) -- both read directly from SkillPrerequisite, the same table
    /skills/readiness already uses, never a separately-invented relationship."""
    skill = db.query(Skill).filter(Skill.key == skill_key).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    prereq_rows = db.query(SkillPrerequisite).filter(SkillPrerequisite.skill_id == skill.id).all()
    prereq_skills = [db.query(Skill).filter(Skill.id == r.prerequisite_skill_id).first() for r in prereq_rows]

    unlock_rows = db.query(SkillPrerequisite).filter(SkillPrerequisite.prerequisite_skill_id == skill.id).all()
    unlock_skills = [db.query(Skill).filter(Skill.id == r.skill_id).first() for r in unlock_rows]

    def node(s: Skill) -> ConceptMapNodeOut:
        return ConceptMapNodeOut(key=s.key, name=s.name, chapter=s.chapter)

    return ConceptMapOut(
        current=node(skill),
        prerequisites=[node(s) for s in prereq_skills if s],
        unlocks=[node(s) for s in unlock_skills if s],
    )


@router.get("/{skill_key}/transfer-challenge", response_model=TransferChallengeOut)
def get_transfer_challenge(
    skill_key: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Anti-memorization check (spec section 52): once a skill looks mastered on
    familiar problems, surface a *different*, not-yet-attempted problem in the same
    skill -- submitting it in transfer mode measures whether the understanding
    actually generalizes, rather than recommending "solve Two Sum again"."""
    skill = db.query(Skill).filter(Skill.key == skill_key).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    user_skill = db.query(UserSkill).filter(
        UserSkill.user_id == current_user.id, UserSkill.skill_id == skill.id
    ).first()
    if not user_skill or user_skill.mastery < TRANSFER_MASTERY_THRESHOLD:
        return TransferChallengeOut(
            available=False, reason=f"Mastery on familiar problems is below {int(TRANSFER_MASTERY_THRESHOLD * 100)}% -- "
                                     "solve more problems in this skill before testing transfer.",
        )

    attempted_ids = {
        s.problem_id for s in db.query(Submission).filter(
            Submission.user_id == current_user.id, Submission.problem_id.in_(
                db.query(Problem.id).filter(Problem.primary_skill_id == skill.id)
            )
        ).all()
    }
    candidate = (
        db.query(Problem)
        .filter(Problem.primary_skill_id == skill.id, ~Problem.id.in_(attempted_ids or [""]))
        .first()
    )
    if not candidate:
        return TransferChallengeOut(
            available=False,
            reason="No unattempted problem exists yet in this skill to test transfer against -- you've covered every seeded problem here.",
        )

    return TransferChallengeOut(
        available=True, problem_slug=candidate.slug, problem_title=candidate.title,
        reason=f"Mastery is {int(user_skill.mastery * 100)}% on familiar problems -- this checks whether that "
               "understanding transfers to a problem you haven't seen before.",
    )


@router.get("/graph/mine", response_model=list[UserSkillOut])
def my_skill_graph(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    out = []
    for us in rows:
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if not skill:
            continue
        pr_acc = (us.pattern_recognition_correct / us.pattern_recognition_attempts) if us.pattern_recognition_attempts else None
        tr_acc = (us.transfer_correct / us.transfer_attempts) if us.transfer_attempts else None
        out.append(UserSkillOut(
            skill_key=skill.key, skill_name=skill.name, chapter=skill.chapter,
            mastery=us.mastery, confidence=us.confidence, attempts=us.attempts,
            correct_attempts=us.correct_attempts,
            pattern_recognition_accuracy=pr_acc, transfer_accuracy=tr_acc,
        ))
    return out
