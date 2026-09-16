"""
Recommendation engine (spec sections 61-62): rule-based over the skill graph,
mastery, retention due-dates, and transfer scores. Every recommendation carries
WHAT / WHY / EXPECTED OUTCOME built from the same numbers shown on the dashboard
-- never an unexplained suggestion.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.problem import Problem, Difficulty
from app.models.retention import RetentionReview
from app.models.skill import Skill, UserSkill
from app.services.skill_graph.graph import prerequisites_met

WEAK_THRESHOLD = 0.55
STRONG_THRESHOLD = 0.75


def _ratio(correct: int, attempts: int) -> float | None:
    return round(correct / attempts, 3) if attempts > 0 else None


def build_recommendations(db: Session, user_id: str, limit: int = 5) -> list[dict]:
    recs: list[dict] = []

    # 1) Overdue retention reviews take top priority -- forgetting is the most
    #    time-sensitive failure mode.
    now = datetime.utcnow()
    overdue = (
        db.query(RetentionReview)
        .filter(RetentionReview.user_id == user_id, RetentionReview.due_at <= now)
        .order_by(RetentionReview.due_at.asc())
        .limit(3)
        .all()
    )
    for rr in overdue:
        skill = db.query(Skill).filter(Skill.id == rr.skill_id).first()
        if not skill:
            continue
        days_overdue = max(0, (now - rr.due_at).days)
        recs.append({
            "activity_type": "RETENTION_REVIEW",
            "skill_id": skill.id,
            "problem_id": None,
            "reason_what": f"Quick retrieval review: {skill.name}",
            "reason_why": f"This skill was due for spaced review {days_overdue} day(s) ago; retrieval strength decays without it.",
            "expected_outcome": "Refresh recall before it decays further and reset the review interval.",
            "priority_score": 100 + days_overdue,
        })

    # 2) Weak skills whose prerequisites are already met.
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id, UserSkill.attempts > 0).all()
    for us in user_skills:
        if us.mastery >= WEAK_THRESHOLD:
            continue
        skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if not skill:
            continue
        ready, unmet = prerequisites_met(db, user_id, skill.id)
        if not ready:
            continue
        pr_acc = _ratio(us.pattern_recognition_correct, us.pattern_recognition_attempts)
        if pr_acc is not None and pr_acc < 0.6:
            recs.append({
                "activity_type": "PATTERN_DRILL",
                "skill_id": skill.id,
                "problem_id": None,
                "reason_what": f"Pattern recognition drill: {skill.name}",
                "reason_why": (
                    f"You solved problems tagged {skill.name} but identified the pattern correctly "
                    f"only {pr_acc * 100:.0f}% of the time -- mastery ({us.mastery * 100:.0f}%) is capped by recognition, not coding."
                ),
                "expected_outcome": "Improve pattern recognition before attempting another problem at this level.",
                "priority_score": 80 + (1 - pr_acc) * 20,
            })
        else:
            recs.append({
                "activity_type": "LESSON",
                "skill_id": skill.id,
                "problem_id": None,
                "reason_what": f"Revisit concept lesson: {skill.name}",
                "reason_why": f"Mastery is {us.mastery * 100:.0f}% after {us.attempts} attempt(s) -- below the {WEAK_THRESHOLD*100:.0f}% threshold.",
                "expected_outcome": "Rebuild the underlying concept before more practice problems.",
                "priority_score": 70,
            })

    # 3) Transfer gaps: mastered on familiar problems but not on unfamiliar variants.
    for us in user_skills:
        if us.mastery < STRONG_THRESHOLD:
            continue
        tr_acc = _ratio(us.transfer_correct, us.transfer_attempts)
        if us.transfer_attempts >= 1 and tr_acc is not None and tr_acc < 0.6:
            skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
            recs.append({
                "activity_type": "TRANSFER",
                "skill_id": skill.id,
                "problem_id": None,
                "reason_what": f"Unfamiliar-variant problem: {skill.name}",
                "reason_why": (
                    f"Mastery on familiar problems is {us.mastery*100:.0f}%, but transfer accuracy on unfamiliar "
                    f"variants is only {tr_acc*100:.0f}% -- this looks like memorization, not understanding."
                ),
                "expected_outcome": "Confirm the concept generalizes to a problem shape you haven't seen before.",
                "priority_score": 65,
            })

    # 4) Next unstarted skill whose prerequisites are met (curriculum progression).
    if len(recs) < limit:
        all_skills = db.query(Skill).order_by(Skill.level.asc()).all()
        started_ids = {us.skill_id for us in db.query(UserSkill).filter(UserSkill.user_id == user_id).all()}
        for skill in all_skills:
            if skill.id in started_ids:
                continue
            ready, unmet = prerequisites_met(db, user_id, skill.id)
            if ready:
                recs.append({
                    "activity_type": "LESSON",
                    "skill_id": skill.id,
                    "problem_id": None,
                    "reason_what": f"Start new topic: {skill.name}",
                    "reason_why": "Prerequisites are met and this is the next unstarted skill in your roadmap.",
                    "expected_outcome": "Build the foundation for this topic's practice problems.",
                    "priority_score": 50,
                })
                break

    # 5) Fill remaining slots with a problem recommendation tied to the weakest active skill.
    if user_skills:
        weakest = min(user_skills, key=lambda u: u.mastery)
        skill = db.query(Skill).filter(Skill.id == weakest.skill_id).first()
        target_difficulty = Difficulty.easy if weakest.mastery < 0.4 else Difficulty.medium
        problem = (
            db.query(Problem)
            .filter(Problem.primary_skill_id == weakest.skill_id, Problem.difficulty == target_difficulty)
            .first()
        )
        if problem:
            recs.append({
                "activity_type": "EASY_PROBLEM" if target_difficulty == Difficulty.easy else "MEDIUM_PROBLEM",
                "skill_id": skill.id if skill else None,
                "problem_id": problem.id,
                "reason_what": f"Practice problem: {problem.title}",
                "reason_why": f"Targets your weakest active skill ({skill.name if skill else 'unknown'} at {weakest.mastery*100:.0f}% mastery).",
                "expected_outcome": "Directly raise mastery on the skill currently limiting your progress.",
                "priority_score": 40,
            })

    recs.sort(key=lambda r: r["priority_score"], reverse=True)
    return recs[:limit]
