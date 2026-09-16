"""
Track tier advancement: Novice -> Practitioner -> Expert, one badge each for
the "dsa" track and the "system_design" track (not per-skill, not per-chapter
-- a learner's whole competence in an entire track).

Design, per explicit user direction:
- Starting an assessment is NEVER gated on mastery -- any learner can attempt
  the next tier's assessment at any time (as long as they aren't already at
  the top tier). Mastery is shown purely as informational context ("how much
  have you learnt so far"); it is the assessment itself -- fresh
  problems/cases, solved for real, scored against PASS_CUTOFF below -- that
  gatekeeps tier advancement, never a mastery threshold standing in front of
  it. (An earlier version of this required every skill to individually clear
  85% mastery before the assessment button even appeared -- in practice that
  meant almost nobody could ever see it, since clearing dozens of skills that
  high is a long road. Removed entirely in favor of "just attempt it and see.")
- Starting an assessment always deals a fresh random draw, even if one is
  already in progress -- the previous attempt is marked "abandoned" rather
  than blocking the new one. (An earlier version blocked a second start while
  one was in progress, which meant navigating away from the page and back --
  a browser back button, revisiting later -- kept resurfacing the exact same
  items indefinitely, which is precisely the "same questions keep coming"
  problem this was built to avoid.) The frontend never auto-resumes an
  in-progress assessment on its own either -- only an explicit "start"
  click surfaces one, so a plain revisit always shows a clean slate.
- The two theory-only skills (Algorithmic Thinking & Complexity has zero
  seeded coding problems; Programming Foundations is treated as conceptual
  too) don't have a practical mastery signal at all -- they're checked by a
  real quiz instead (see QuizQuestion), included as items *inside* the DSA
  assessment itself alongside coding problems from several other skills.
- Passing an assessment is an AGGREGATE score across every item (coding
  problems + theory quiz questions for "dsa"; case studies for
  "system_design"), not an all-or-nothing "every single item perfect" bar.
  Each item contributes a 0..1 score built only from real, already-existing
  signals (never invented): a DSA problem scores 1.0 if solved hint-free with
  the correct pattern declared (0.5 if also flagged brute-force at the
  Expert tier, since it's still a real solve just not the intended
  complexity), 0.6 if solved but with a hint used or without correctly
  declaring the pattern first, 0.0 if not solved yet; a quiz question scores
  1.0 or 0.0 (exact-match grading); a system design case scores its own
  real critique score for the most recent fresh attempt made since the
  assessment started. The assessment resolves once every item has at least
  one attempt; it passes if the mean of all item scores is >= PASS_CUTOFF.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.problem import Problem
from app.models.quiz import QuizAttempt, QuizQuestion
from app.models.skill import Skill, UserSkill
from app.models.submission import ReasoningAttempt, Submission, SubmissionStatus
from app.models.system_design import SystemDesignAttempt, SystemDesignCase
from app.models.track_tier import TrackTierAssessment, UserTrackTier

TIER_ORDER = ["novice", "practitioner", "expert"]
TRACKS = ["dsa", "system_design"]

THEORY_SKILL_KEYS = {"ALGORITHMIC_THINKING", "PROGRAMMING_BASICS"}

PASS_CUTOFF = 0.85  # aggregate score across all assessment items needed to pass

DSA_PROBLEM_ITEM_COUNT = 5
DSA_QUIZ_ITEM_COUNT = 3

SCALE_FOR_TIER = {"practitioner": "growth", "expert": "global"}


def next_tier(current_tier: str) -> str | None:
    idx = TIER_ORDER.index(current_tier) if current_tier in TIER_ORDER else 0
    return TIER_ORDER[idx + 1] if idx + 1 < len(TIER_ORDER) else None


@dataclass
class TrackStatus:
    current_tier: str
    next_tier: str | None
    detail: str
    active_assessment_id: str | None = None


def _dsa_avg_mastery(db: Session, user_id: str) -> float:
    skills = db.query(Skill).filter(~Skill.key.in_(THEORY_SKILL_KEYS)).all()
    if not skills:
        return 0.0
    total = 0.0
    for s in skills:
        us = db.query(UserSkill).filter(UserSkill.user_id == user_id, UserSkill.skill_id == s.id).first()
        total += us.mastery if us else 0.0
    return total / len(skills)


def _sd_avg_score(db: Session, user_id: str) -> float:
    families = [r[0] for r in db.query(SystemDesignCase.base_slug).distinct().all() if r[0]]
    if not families:
        return 0.0
    total = 0.0
    for fam in families:
        case_ids = [c.id for c in db.query(SystemDesignCase.id).filter(SystemDesignCase.base_slug == fam).all()]
        best = (
            db.query(SystemDesignAttempt)
            .filter(SystemDesignAttempt.user_id == user_id, SystemDesignAttempt.case_id.in_(case_ids))
            .order_by(SystemDesignAttempt.score.desc())
            .first()
        )
        total += best.score if best else 0.0
    return total / len(families)


def get_track_status(db: Session, user_id: str, track: str) -> TrackStatus:
    row = db.query(UserTrackTier).filter(UserTrackTier.user_id == user_id, UserTrackTier.track == track).first()
    current = row.tier if row else "novice"
    nxt = next_tier(current)

    active = (
        db.query(TrackTierAssessment)
        .filter(TrackTierAssessment.user_id == user_id, TrackTierAssessment.track == track, TrackTierAssessment.status == "in_progress")
        .order_by(TrackTierAssessment.created_at.desc())
        .first()
    )

    if nxt is None:
        return TrackStatus(current, None, "Top tier already reached.", active.id if active else None)

    avg = _dsa_avg_mastery(db, user_id) if track == "dsa" else _sd_avg_score(db, user_id)
    what = "average mastery across DSA skills" if track == "dsa" else "average best score across case families"
    detail = (
        f"{what}: {int(avg * 100)}% (informational only -- passing a real {nxt} assessment is what "
        "advances the tier, not mastery)."
    )

    return TrackStatus(current, nxt, detail, active.id if active else None)


@dataclass
class ItemRef:
    kind: str  # "problem" | "quiz" | "case"
    id: str
    slug: str
    title: str
    options: list[str] | None = None


@dataclass
class StartResult:
    ok: bool
    reason: str | None = None
    assessment: TrackTierAssessment | None = None
    items: list[ItemRef] = field(default_factory=list)


def _pick_dsa_items(db: Session, user_id: str, target_tier: str) -> list[ItemRef]:
    # Randomized on purpose: a fixed, always-identical set of questions could
    # just be memorized answer-by-answer instead of actually demonstrating the
    # skill, so each new assessment attempt draws a fresh random selection.
    skills = db.query(Skill).filter(~Skill.key.in_(THEORY_SKILL_KEYS)).all()
    chosen_skills = random.sample(skills, min(DSA_PROBLEM_ITEM_COUNT, len(skills)))
    already_passed = {
        s.problem_id for s in db.query(Submission).filter(Submission.user_id == user_id, Submission.status == SubmissionStatus.passed).all()
    }
    items: list[ItemRef] = []
    for skill in chosen_skills:
        pool = db.query(Problem).filter(Problem.primary_skill_id == skill.id).all()
        if not pool:
            continue
        unsolved = [p for p in pool if p.id not in already_passed]
        candidates = unsolved or pool
        if target_tier == "expert":
            preferred = [p for p in candidates if p.difficulty.value in ("medium", "hard", "expert")]
            candidates = preferred or candidates
        p = random.choice(candidates)
        items.append(ItemRef(kind="problem", id=p.id, slug=p.slug, title=p.title))

    quiz_pool = db.query(QuizQuestion).join(Skill, Skill.id == QuizQuestion.skill_id).filter(Skill.key.in_(THEORY_SKILL_KEYS)).all()
    chosen_quiz = random.sample(quiz_pool, min(DSA_QUIZ_ITEM_COUNT, len(quiz_pool)))
    for q in chosen_quiz:
        items.append(ItemRef(kind="quiz", id=q.id, slug=q.id, title=q.question, options=q.options))

    return items


def _pick_sd_items(db: Session, target_tier: str) -> list[ItemRef]:
    scale = SCALE_FOR_TIER[target_tier]
    families = [r[0] for r in db.query(SystemDesignCase.base_slug).distinct().all() if r[0]]
    items = []
    for fam in families:
        case = db.query(SystemDesignCase).filter(SystemDesignCase.base_slug == fam, SystemDesignCase.scale_tier == scale).first()
        if case:
            items.append(ItemRef(kind="case", id=case.id, slug=case.slug, title=case.title))
    return items


def start_track_assessment(db: Session, user_id: str, track: str) -> StartResult:
    status = get_track_status(db, user_id, track)
    if status.next_tier is None:
        return StartResult(False, "This track is already at the top tier (Expert).")

    # Starting fresh always wins over a stale in-progress attempt -- a learner
    # who navigates away and back (or explicitly starts again) gets a new
    # random draw rather than being stuck re-seeing the same items forever.
    # The abandoned attempt is marked, not deleted, and is simply never
    # reachable again since nothing looks it up by anything but its own id.
    if status.active_assessment_id:
        stale = db.query(TrackTierAssessment).filter(TrackTierAssessment.id == status.active_assessment_id).first()
        if stale:
            stale.status = "abandoned"
            stale.resolved_at = datetime.utcnow()

    items = _pick_dsa_items(db, user_id, status.next_tier) if track == "dsa" else _pick_sd_items(db, status.next_tier)
    if not items:
        return StartResult(False, "No assessment items are available yet for this track/tier.")

    assessment = TrackTierAssessment(
        user_id=user_id, track=track, target_tier=status.next_tier,
        item_ids=[{"kind": i.kind, "id": i.id} for i in items], status="in_progress",
    )
    db.add(assessment)
    db.flush()
    return StartResult(True, assessment=assessment, items=items)


@dataclass
class ItemCheck:
    kind: str
    slug: str
    title: str
    attempted: bool
    score: float
    passed: bool
    reason: str
    options: list[str] | None = None


@dataclass
class CheckResult:
    status: str  # "in_progress" | "passed" | "failed"
    checks: list[ItemCheck]
    aggregate_score: float | None = None


def _reran_brute_force_check(submission: Submission, problem: Problem) -> str | None:
    from app.routers.problems import COMPLEXITY_CLASS, _analyze_submission
    from app.services.diagnosis.engine import detect_brute_force
    from app.services.execution.starter_code import function_name_for_language

    language = submission.language or "python"
    call_name = function_name_for_language(problem.function_name, language)
    try:
        code_features = _analyze_submission(submission.code, call_name, language)
    except Exception:
        return None
    expected_class = COMPLEXITY_CLASS.get(problem.expected_complexity, 1)
    return detect_brute_force(code_features, expected_class, problem.expected_complexity)


def _check_dsa_problem(db: Session, assessment: TrackTierAssessment, problem: Problem) -> ItemCheck:
    submission = (
        db.query(Submission)
        .filter(
            Submission.user_id == assessment.user_id, Submission.problem_id == problem.id,
            Submission.created_at >= assessment.created_at, Submission.status == SubmissionStatus.passed,
        )
        .order_by(Submission.created_at.desc())
        .first()
    )
    if submission is None:
        return ItemCheck("problem", problem.slug, problem.title, False, 0.0, False, "Not solved yet since this assessment started.")

    reasoning = (
        db.query(ReasoningAttempt)
        .filter(ReasoningAttempt.user_id == assessment.user_id, ReasoningAttempt.problem_id == problem.id, ReasoningAttempt.created_at >= assessment.created_at)
        .order_by(ReasoningAttempt.created_at.desc())
        .first()
    )
    hint_free = not submission.hint_count_used
    correct_pattern = bool(reasoning and reasoning.is_correct_pattern)

    if hint_free and correct_pattern:
        if assessment.target_tier == "expert" and _reran_brute_force_check(submission, problem):
            return ItemCheck("problem", problem.slug, problem.title, True, 0.5, False, "Solved correctly, but flagged as brute-force -- Expert requires the intended-complexity approach (partial credit).")
        return ItemCheck("problem", problem.slug, problem.title, True, 1.0, True, "Solved hint-free with the correct pattern declared.")

    reason = "Solved, but "
    reason += "used a hint" if not hint_free else "the pattern wasn't correctly declared first"
    return ItemCheck("problem", problem.slug, problem.title, True, 0.6, False, reason + " (partial credit).")


def _check_quiz(db: Session, assessment: TrackTierAssessment, question: QuizQuestion) -> ItemCheck:
    attempt = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.user_id == assessment.user_id, QuizAttempt.question_id == question.id, QuizAttempt.created_at >= assessment.created_at)
        .order_by(QuizAttempt.created_at.desc())
        .first()
    )
    if attempt is None:
        return ItemCheck("quiz", question.id, question.question, False, 0.0, False, "Not answered yet since this assessment started.", options=question.options)
    if attempt.is_correct:
        return ItemCheck("quiz", question.id, question.question, True, 1.0, True, "Correct.", options=question.options)
    return ItemCheck("quiz", question.id, question.question, True, 0.0, False, "Incorrect.", options=question.options)


def _check_sd_case(db: Session, assessment: TrackTierAssessment, case: SystemDesignCase) -> ItemCheck:
    attempts = (
        db.query(SystemDesignAttempt)
        .filter(SystemDesignAttempt.user_id == assessment.user_id, SystemDesignAttempt.case_id == case.id, SystemDesignAttempt.created_at >= assessment.created_at)
        .order_by(SystemDesignAttempt.created_at.desc())
        .all()
    )
    if not attempts:
        return ItemCheck("case", case.slug, case.title, False, 0.0, False, "Not attempted yet since this assessment started.")

    best = max(attempts, key=lambda a: a.score)
    passed = best.score >= PASS_CUTOFF
    reason = f"Best attempt scored {int(best.score * 100)}%."
    fb = best.feedback or {}
    notes = []
    if fb.get("missing_components"):
        notes.append(f"missing {', '.join(fb['missing_components'])}")
    if fb.get("unjustified_components"):
        notes.append(f"unjustified {', '.join(fb['unjustified_components'])}")
    if notes:
        reason += " (" + "; ".join(notes) + ")"
    return ItemCheck("case", case.slug, case.title, True, best.score, passed, reason)


def check_track_assessment(db: Session, assessment: TrackTierAssessment) -> CheckResult:
    checks: list[ItemCheck] = []
    if assessment.track == "dsa":
        problem_ids = [i["id"] for i in assessment.item_ids if i["kind"] == "problem"]
        quiz_ids = [i["id"] for i in assessment.item_ids if i["kind"] == "quiz"]
        problems = {p.id: p for p in db.query(Problem).filter(Problem.id.in_(problem_ids)).all()}
        questions = {q.id: q for q in db.query(QuizQuestion).filter(QuizQuestion.id.in_(quiz_ids)).all()}
        for item in assessment.item_ids:
            if item["kind"] == "problem":
                p = problems.get(item["id"])
                checks.append(_check_dsa_problem(db, assessment, p) if p else ItemCheck("problem", "?", "?", False, 0.0, False, "Problem no longer exists."))
            else:
                q = questions.get(item["id"])
                checks.append(_check_quiz(db, assessment, q) if q else ItemCheck("quiz", "?", "?", False, 0.0, False, "Question no longer exists."))
    else:
        case_ids = [i["id"] for i in assessment.item_ids]
        cases = {c.id: c for c in db.query(SystemDesignCase).filter(SystemDesignCase.id.in_(case_ids)).all()}
        for item in assessment.item_ids:
            c = cases.get(item["id"])
            checks.append(_check_sd_case(db, assessment, c) if c else ItemCheck("case", "?", "?", False, 0.0, False, "Case no longer exists."))

    if any(not c.attempted for c in checks):
        return CheckResult("in_progress", checks)

    aggregate = sum(c.score for c in checks) / len(checks)
    status = "passed" if aggregate >= PASS_CUTOFF else "failed"
    return CheckResult(status, checks, aggregate)


def resolve_track_assessment(db: Session, assessment: TrackTierAssessment, result: CheckResult) -> None:
    assessment.status = result.status
    assessment.results = [
        {"kind": c.kind, "slug": c.slug, "title": c.title, "score": c.score, "passed": c.passed, "reason": c.reason, "options": c.options}
        for c in result.checks
    ]
    if result.aggregate_score is not None:
        assessment.aggregate_score = result.aggregate_score
    if result.status in ("passed", "failed"):
        assessment.resolved_at = datetime.utcnow()
    if result.status == "passed":
        row = db.query(UserTrackTier).filter(UserTrackTier.user_id == assessment.user_id, UserTrackTier.track == assessment.track).first()
        if row:
            row.tier = assessment.target_tier
        else:
            db.add(UserTrackTier(user_id=assessment.user_id, track=assessment.track, tier=assessment.target_tier))
