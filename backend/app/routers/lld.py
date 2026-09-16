from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.system_design import LLDAttempt, LLDCase
from app.models.user import User
from app.schemas.lld import LLDAttemptRequest, LLDAttemptResponse, LLDCaseOut
from app.services.system_design.lld_critique import critique_lld_design

router = APIRouter(prefix="/lld", tags=["lld"])


@router.get("/cases", response_model=list[LLDCaseOut])
def list_cases(db: Session = Depends(get_db)):
    return db.query(LLDCase).all()


@router.get("/cases/{slug}", response_model=LLDCaseOut)
def get_case(slug: str, db: Session = Depends(get_db)):
    case = db.query(LLDCase).filter(LLDCase.slug == slug).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.post("/cases/{slug}/attempt", response_model=LLDAttemptResponse)
def attempt_case(
    slug: str, payload: LLDAttemptRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    case = db.query(LLDCase).filter(LLDCase.slug == slug).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    classes = [c.model_dump() for c in payload.classes]
    result = critique_lld_design(classes, case.expected_classes)

    db.add(LLDAttempt(user_id=current_user.id, case_id=case.id, classes=classes, feedback=result, score=result["score"]))
    db.commit()

    return LLDAttemptResponse(**result)
