from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.contest import Contest, ContestSubmission
from app.models.problem import Problem
from app.models.user import User
from app.schemas.contest import (
    ContestDetailOut, ContestOut, ContestProblemOut, ContestSubmitRequest, LeaderboardEntryOut,
)
from app.schemas.problem import SubmitRequest, SubmitResponse
from app.routers.problems import submit_solution

router = APIRouter(prefix="/contests", tags=["contests"])

# Simple time-decay scoring, same spirit as competitive-programming judges:
# solving early in the window is worth more than solving right before it
# closes, but every genuine pass still earns a real, non-trivial score.
CONTEST_MAX_POINTS = 100.0
CONTEST_MIN_POINTS = 20.0
CONTEST_DECAY_PER_MINUTE = 1.0


def _status(contest: Contest) -> str:
    now = datetime.utcnow()
    if now < contest.start_at:
        return "upcoming"
    if now > contest.end_at:
        return "ended"
    return "live"


@router.get("", response_model=list[ContestOut])
def list_contests(db: Session = Depends(get_db)):
    contests = db.query(Contest).order_by(Contest.start_at.desc()).all()
    return [
        ContestOut(
            id=c.id, title=c.title, start_at=c.start_at, end_at=c.end_at,
            status=_status(c), problem_count=len(c.problem_ids or []),
        )
        for c in contests
    ]


@router.get("/{contest_id}", response_model=ContestDetailOut)
def get_contest(contest_id: str, db: Session = Depends(get_db)):
    contest = db.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(status_code=404, detail="Contest not found")

    status = _status(contest)
    problems_out: list[ContestProblemOut] = []
    if status != "upcoming":
        problems_by_id = {p.id: p for p in db.query(Problem).filter(Problem.id.in_(contest.problem_ids or [])).all()}
        for pid in contest.problem_ids or []:
            p = problems_by_id.get(pid)
            if p:
                problems_out.append(ContestProblemOut(slug=p.slug, title=p.title, difficulty=p.difficulty.value))

    return ContestDetailOut(
        id=contest.id, title=contest.title, start_at=contest.start_at, end_at=contest.end_at,
        status=status, problem_count=len(contest.problem_ids or []), problems=problems_out,
    )


@router.post("/{contest_id}/problems/{slug}/submit", response_model=SubmitResponse)
def submit_contest_solution(
    contest_id: str, slug: str, payload: ContestSubmitRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    contest = db.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(status_code=404, detail="Contest not found")

    status = _status(contest)
    if status == "upcoming":
        raise HTTPException(status_code=400, detail="This contest hasn't started yet.")

    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem or problem.id not in (contest.problem_ids or []):
        raise HTTPException(status_code=404, detail="This problem isn't part of this contest.")

    # Reuse the exact same grading pipeline every other submission goes
    # through (compile/run against every real test case, mastery update,
    # diagnosis) -- contest mode is never a separate, weaker judge.
    result = submit_solution(
        slug, SubmitRequest(code=payload.code, language=payload.language, mode="contest"),
        current_user, db,
    )

    if status == "live" and result.status == "PASSED":
        already_scored = db.query(ContestSubmission).filter(
            ContestSubmission.contest_id == contest.id, ContestSubmission.user_id == current_user.id,
            ContestSubmission.problem_id == problem.id,
        ).first()
        if not already_scored:
            minutes_elapsed = (datetime.utcnow() - contest.start_at).total_seconds() / 60
            score = max(CONTEST_MIN_POINTS, CONTEST_MAX_POINTS - CONTEST_DECAY_PER_MINUTE * minutes_elapsed)
            db.add(ContestSubmission(
                contest_id=contest.id, user_id=current_user.id, problem_id=problem.id,
                submission_id=result.submission_id, score=round(score, 1),
            ))
            db.commit()

    return result


@router.get("/{contest_id}/leaderboard", response_model=list[LeaderboardEntryOut])
def contest_leaderboard(contest_id: str, db: Session = Depends(get_db)):
    contest = db.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(status_code=404, detail="Contest not found")

    rows = db.query(ContestSubmission).filter(ContestSubmission.contest_id == contest_id).all()
    totals: dict[str, dict] = {}
    for r in rows:
        entry = totals.setdefault(r.user_id, {"score": 0.0, "solved": 0})
        entry["score"] += r.score
        entry["solved"] += 1

    ranked = sorted(totals.items(), key=lambda kv: (-kv[1]["score"], -kv[1]["solved"]))
    out = []
    for rank, (user_id, agg) in enumerate(ranked, start=1):
        user = db.query(User).filter(User.id == user_id).first()
        out.append(LeaderboardEntryOut(
            rank=rank, user_name=user.name if user else "?",
            total_score=round(agg["score"], 1), problems_solved=agg["solved"],
        ))
    return out
