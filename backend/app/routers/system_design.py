from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.system_design import SystemDesignAttempt, SystemDesignCase, SystemDesignLesson
from app.models.user import User
from app.schemas.lesson_coach import AskLessonRequest, AskLessonResponse, ExplainBackRequest, ExplainBackResponse
from app.schemas.system_design import (
    LessonConceptMapNodeOut, LessonConceptMapOut, SystemDesignAttemptRequest, SystemDesignAttemptResponse,
    SystemDesignCaseOut, SystemDesignLessonOut,
)
from app.services.coach.explain_back_scorer import score_explanation
from app.services.coach.sd_scope_detector import predict_scope
from app.services.llm.lesson_qa import LocalLLMUnavailable, ask_about_lesson
from app.services.system_design.critique import critique_architecture, grade_estimation

router = APIRouter(prefix="/system-design", tags=["system-design"])


@router.get("/lessons", response_model=list[SystemDesignLessonOut])
def list_lessons(level: int | None = None, db: Session = Depends(get_db)):
    q = db.query(SystemDesignLesson)
    if level is not None:
        q = q.filter(SystemDesignLesson.level == level)
    return q.order_by(SystemDesignLesson.level.asc()).all()


@router.post("/lessons/{slug}/ask", response_model=AskLessonResponse)
def ask_about_sd_lesson(slug: str, payload: AskLessonRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lesson = db.query(SystemDesignLesson).filter(SystemDesignLesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    try:
        answer = ask_about_lesson(lesson.title, lesson.content_markdown, payload.question)
    except LocalLLMUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))
    return AskLessonResponse(answer=answer)


@router.post("/lessons/{slug}/explain-back", response_model=ExplainBackResponse)
def explain_sd_lesson_back(slug: str, payload: ExplainBackRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lesson = db.query(SystemDesignLesson).filter(SystemDesignLesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return ExplainBackResponse(**score_explanation(lesson.title, lesson.content_markdown, payload.explanation))


@router.get("/lessons/{slug}/concept-map", response_model=LessonConceptMapOut)
def get_lesson_concept_map(slug: str, db: Session = Depends(get_db)):
    """Orientation graphic data: since system design lessons don't have an
    authored prerequisite graph the way DSA skills do, 'previous'/'next' are a
    real, honest, deterministic relationship -- the nearest lower/higher-level
    lesson in the SAME category -- not a fabricated dependency."""
    lesson = db.query(SystemDesignLesson).filter(SystemDesignLesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    same_category = (
        db.query(SystemDesignLesson)
        .filter(SystemDesignLesson.category == lesson.category)
        .order_by(SystemDesignLesson.level.asc())
        .all()
    )
    idx = next((i for i, l in enumerate(same_category) if l.id == lesson.id), None)
    prev_lesson = same_category[idx - 1] if idx is not None and idx > 0 else None
    next_lesson = same_category[idx + 1] if idx is not None and idx + 1 < len(same_category) else None

    def node(l: SystemDesignLesson) -> LessonConceptMapNodeOut:
        return LessonConceptMapNodeOut(slug=l.slug, title=l.title, category=l.category, level=l.level)

    return LessonConceptMapOut(
        current=node(lesson),
        previous=node(prev_lesson) if prev_lesson else None,
        next=node(next_lesson) if next_lesson else None,
    )


@router.get("/cases", response_model=list[SystemDesignCaseOut])
def list_cases(db: Session = Depends(get_db)):
    return db.query(SystemDesignCase).all()


@router.get("/cases/{slug}", response_model=SystemDesignCaseOut)
def get_case(slug: str, db: Session = Depends(get_db)):
    case = db.query(SystemDesignCase).filter(SystemDesignCase.slug == slug).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.post("/cases/{slug}/attempt", response_model=SystemDesignAttemptResponse)
def attempt_case(
    slug: str, payload: SystemDesignAttemptRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    case = db.query(SystemDesignCase).filter(SystemDesignCase.slug == slug).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    nodes = [n.model_dump() for n in payload.nodes]
    edges = [e.model_dump() for e in payload.edges]
    critique = critique_architecture(nodes, edges, case.expected_components)
    estimation_feedback = grade_estimation(payload.estimation_answers, case.estimation_expected)
    scope_coach = predict_scope(
        case.scale_tier, len(nodes), len(critique["missing_components"]), len(critique["unjustified_components"]),
    )

    attempt = SystemDesignAttempt(
        user_id=current_user.id, case_id=case.id,
        architecture={"nodes": nodes, "edges": edges}, estimation_answers=payload.estimation_answers,
        feedback={**critique, "estimation": estimation_feedback}, score=critique["score"],
    )
    db.add(attempt)
    db.commit()

    return SystemDesignAttemptResponse(
        score=critique["score"], missing_components=critique["missing_components"],
        unjustified_components=critique["unjustified_components"],
        estimation_feedback=estimation_feedback, why_questions=critique["why_questions"],
        scope_coach=scope_coach,
    )
