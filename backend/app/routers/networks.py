from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.network import NetworkLesson, NetworkQuizAttempt, NetworkQuizQuestion
from app.models.user import User
from app.schemas.lesson_coach import AskLessonRequest, AskLessonResponse, ExplainBackRequest, ExplainBackResponse
from app.schemas.network import (
    NetworkConceptMapNodeOut, NetworkConceptMapOut, NetworkLessonOut,
    NetworkQuizAnswerIn, NetworkQuizAnswerOut, NetworkQuizQuestionOut,
)
from app.services.coach.explain_back_scorer import score_explanation
from app.services.llm.lesson_qa import LocalLLMUnavailable, ask_about_lesson

router = APIRouter(prefix="/networks", tags=["networks"])


@router.get("/lessons", response_model=list[NetworkLessonOut])
def list_lessons(db: Session = Depends(get_db)):
    return db.query(NetworkLesson).order_by(NetworkLesson.level.asc()).all()


@router.get("/lessons/{slug}/concept-map", response_model=NetworkConceptMapOut)
def get_lesson_concept_map(slug: str, db: Session = Depends(get_db)):
    """Same honest fallback as the System Design lesson concept-map: no
    authored prerequisite graph exists for this curriculum, so 'previous'/
    'next' is the nearest lower/higher-level lesson in the same category --
    a real, deterministic relationship, not a fabricated dependency."""
    lesson = db.query(NetworkLesson).filter(NetworkLesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    same_category = (
        db.query(NetworkLesson)
        .filter(NetworkLesson.category == lesson.category)
        .order_by(NetworkLesson.level.asc())
        .all()
    )
    idx = next((i for i, l in enumerate(same_category) if l.id == lesson.id), None)
    prev_lesson = same_category[idx - 1] if idx is not None and idx > 0 else None
    next_lesson = same_category[idx + 1] if idx is not None and idx + 1 < len(same_category) else None

    def node(l: NetworkLesson) -> NetworkConceptMapNodeOut:
        return NetworkConceptMapNodeOut(slug=l.slug, title=l.title, category=l.category, level=l.level)

    return NetworkConceptMapOut(
        current=node(lesson),
        previous=node(prev_lesson) if prev_lesson else None,
        next=node(next_lesson) if next_lesson else None,
    )


@router.post("/lessons/{slug}/ask", response_model=AskLessonResponse)
def ask_about_network_lesson(slug: str, payload: AskLessonRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lesson = db.query(NetworkLesson).filter(NetworkLesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    try:
        answer = ask_about_lesson(lesson.title, lesson.content_markdown, payload.question)
    except LocalLLMUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))
    return AskLessonResponse(answer=answer)


@router.post("/lessons/{slug}/explain-back", response_model=ExplainBackResponse)
def explain_network_lesson_back(slug: str, payload: ExplainBackRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lesson = db.query(NetworkLesson).filter(NetworkLesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return ExplainBackResponse(**score_explanation(lesson.title, lesson.content_markdown, payload.explanation))


@router.get("/lessons/{slug}/quiz", response_model=list[NetworkQuizQuestionOut])
def get_lesson_quiz(slug: str, db: Session = Depends(get_db)):
    """Practice questions for one lesson -- immediate, deterministic
    multiple-choice grading, the practice layer this curriculum otherwise
    lacks (no coding problems, no case studies). Never returns correct_index
    to the client -- see the POST answer endpoint for grading."""
    lesson = db.query(NetworkLesson).filter(NetworkLesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    questions = db.query(NetworkQuizQuestion).filter(NetworkQuizQuestion.lesson_id == lesson.id).all()
    return [NetworkQuizQuestionOut(id=q.id, question=q.question, options=q.options) for q in questions]


@router.post("/quiz/answer", response_model=NetworkQuizAnswerOut)
def answer_quiz_question(
    payload: NetworkQuizAnswerIn,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    question = db.query(NetworkQuizQuestion).filter(NetworkQuizQuestion.id == payload.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = payload.selected_index == question.correct_index
    db.add(NetworkQuizAttempt(
        user_id=current_user.id, question_id=question.id,
        selected_index=payload.selected_index, is_correct=is_correct,
    ))
    db.commit()

    return NetworkQuizAnswerOut(correct=is_correct, correct_index=question.correct_index, explanation=question.explanation)
