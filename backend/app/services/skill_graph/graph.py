from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.skill import Skill, SkillPrerequisite, UserSkill

DIFFICULTY_WEIGHT = {"easy": 0.6, "medium": 1.0, "hard": 1.4, "expert": 1.8}


def get_or_create_user_skill(db: Session, user_id: str, skill_id: str) -> UserSkill:
    us = db.query(UserSkill).filter(UserSkill.user_id == user_id, UserSkill.skill_id == skill_id).first()
    if us is None:
        us = UserSkill(user_id=user_id, skill_id=skill_id)
        db.add(us)
        db.flush()
    return us


def update_mastery_from_submission(
    db: Session, user_id: str, skill_id: str, *, correct: bool, difficulty: str,
    is_repeat_solve: bool = False, alpha: float = 0.25,
) -> UserSkill:
    """EWMA mastery update, weighted by difficulty. alpha controls how fast recent
    evidence overrides old mastery -- higher alpha means faster-moving estimate.

    `is_repeat_solve` (a PASSED submission on a problem this user has already
    passed before) sharply dampens the update on a correct result: re-solving a
    problem you've already solved -- especially by re-running code you already
    wrote -- is weak evidence of understanding compared to a fresh problem, and
    letting it move mastery at full strength would let mastery climb from
    repetition rather than actual comprehension. A repeat *failure* isn't
    dampened -- backsliding on a problem you'd solved before is still real
    evidence something isn't retained."""
    us = get_or_create_user_skill(db, user_id, skill_id)
    weight = DIFFICULTY_WEIGHT.get(difficulty, 1.0)
    target = 1.0 if correct else 0.0

    effective_alpha = min(0.6, alpha * weight)
    if is_repeat_solve and correct:
        effective_alpha *= 0.15
    us.mastery = round((1 - effective_alpha) * us.mastery + effective_alpha * target, 4)

    us.attempts += 1
    if correct:
        us.correct_attempts += 1
    us.last_practiced_at = datetime.utcnow()

    # confidence grows with evidence volume, caps out so it never claims certainty from 1 attempt
    us.confidence = round(min(0.95, us.attempts / (us.attempts + 4)), 4)

    return us


def update_pattern_recognition(db: Session, user_id: str, skill_id: str, correct: bool) -> UserSkill:
    us = get_or_create_user_skill(db, user_id, skill_id)
    us.pattern_recognition_attempts += 1
    if correct:
        us.pattern_recognition_correct += 1
    return us


def update_transfer(db: Session, user_id: str, skill_id: str, correct: bool) -> UserSkill:
    us = get_or_create_user_skill(db, user_id, skill_id)
    us.transfer_attempts += 1
    if correct:
        us.transfer_correct += 1
    return us


def prerequisites_met(db: Session, user_id: str, skill_id: str, threshold: float = 0.6) -> tuple[bool, list[str]]:
    """Returns (ready, [unmet prerequisite skill keys])."""
    prereqs = db.query(SkillPrerequisite).filter(SkillPrerequisite.skill_id == skill_id).all()
    unmet = []
    for p in prereqs:
        us = db.query(UserSkill).filter(
            UserSkill.user_id == user_id, UserSkill.skill_id == p.prerequisite_skill_id
        ).first()
        mastery = us.mastery if us else 0.0
        if mastery < threshold:
            prereq_skill = db.query(Skill).filter(Skill.id == p.prerequisite_skill_id).first()
            unmet.append(prereq_skill.key if prereq_skill else p.prerequisite_skill_id)
    return len(unmet) == 0, unmet
