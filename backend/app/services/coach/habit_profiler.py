"""
A real neural network (MLPClassifier) that classifies a student's overall
problem-solving HABITS -- not any single submission's correctness, but
patterns across their whole history -- trained the same way as the existing
diagnosis model (services/diagnosis/model.py): on a large synthetic dataset
whose labels are produced by an explicit, auditable rule function encoding
real coaching judgment, which lets the trained classifier generalize across
feature combinations the rules didn't explicitly enumerate, rather than
being a frozen if/elif ladder.

The FEATURES fed into it at prediction time are never synthetic -- they're
computed live from this specific user's real Submission, ReasoningAttempt,
and HintUsage rows. Only the training LABELS are synthetic-but-rule-grounded,
exactly the same honesty split the diagnosis model already uses.
"""
from __future__ import annotations

import random
from functools import lru_cache

import numpy as np
from sklearn.neural_network import MLPClassifier
from sqlalchemy.orm import Session

from app.models.problem import HintUsage
from app.models.submission import ReasoningAttempt, Submission, SubmissionStatus

HABITS = {
    "STRONG_HABITS": "Plans before coding, rarely needs hints, usually solves in a few tries -- keep doing exactly this.",
    "SKIPS_PLANNING": "Jumps straight to code without stating a plan first -- try declaring your approach (pattern reasoning mode) before writing anything.",
    "HINT_DEPENDENT": "Leans on hints heavily -- try giving yourself 5-10 minutes of genuinely stuck time before reaching for the first hint.",
    "TRIAL_AND_ERROR": "High submission count per problem with little upfront planning -- a sign of guess-and-check rather than reasoning through the approach first.",
    "DEVELOPING": "No single dominant pattern yet -- solid mixed habits, kept improving from here.",
}

FEATURE_NAMES = ["reasoning_usage_rate", "avg_hints_per_problem", "avg_submissions_per_problem", "solve_rate"]

MIN_SUBMISSIONS_FOR_PROFILE = 3


def _label_example(f: dict) -> str:
    if f["reasoning_usage_rate"] >= 0.5 and f["avg_hints_per_problem"] < 0.5 and f["avg_submissions_per_problem"] <= 2.0:
        return "STRONG_HABITS"
    if f["avg_hints_per_problem"] >= 1.5:
        return "HINT_DEPENDENT"
    if f["reasoning_usage_rate"] < 0.2 and f["avg_submissions_per_problem"] >= 3.0:
        return "TRIAL_AND_ERROR"
    if f["reasoning_usage_rate"] < 0.2:
        return "SKIPS_PLANNING"
    return "DEVELOPING"


def _generate_synthetic_dataset(n: int, seed: int = 42):
    rng = random.Random(seed)
    X, y = [], []
    for _ in range(n):
        f = {
            "reasoning_usage_rate": rng.uniform(0.0, 1.0),
            "avg_hints_per_problem": rng.uniform(0.0, 3.0),
            "avg_submissions_per_problem": rng.uniform(1.0, 6.0),
            "solve_rate": rng.uniform(0.2, 1.0),
        }
        label = _label_example(f)
        X.append([f[name] for name in FEATURE_NAMES])
        y.append(label)
    return np.array(X, dtype=float), np.array(y)


@lru_cache(maxsize=1)
def _get_model() -> MLPClassifier:
    X, y = _generate_synthetic_dataset(n=4000)
    clf = MLPClassifier(hidden_layer_sizes=(32, 16), activation="relu", solver="adam", alpha=1e-3, max_iter=2000, random_state=42)
    clf.fit(X, y)
    return clf


def _compute_real_features(db: Session, user_id: str) -> dict | None:
    submissions = db.query(Submission).filter(Submission.user_id == user_id).all()
    if len(submissions) < MIN_SUBMISSIONS_FOR_PROFILE:
        return None

    distinct_problem_ids = {s.problem_id for s in submissions}
    n_problems = len(distinct_problem_ids)

    reasoning_problem_ids = {
        r.problem_id for r in db.query(ReasoningAttempt).filter(ReasoningAttempt.user_id == user_id).all()
    }
    reasoning_usage_rate = len(reasoning_problem_ids & distinct_problem_ids) / n_problems

    n_hints = db.query(HintUsage).filter(HintUsage.user_id == user_id).count()
    avg_hints_per_problem = n_hints / n_problems

    avg_submissions_per_problem = len(submissions) / n_problems

    solved_problem_ids = {s.problem_id for s in submissions if s.status == SubmissionStatus.passed}
    solve_rate = len(solved_problem_ids) / n_problems

    return {
        "reasoning_usage_rate": reasoning_usage_rate,
        "avg_hints_per_problem": avg_hints_per_problem,
        "avg_submissions_per_problem": avg_submissions_per_problem,
        "solve_rate": solve_rate,
        "n_problems_attempted": n_problems,
        "n_submissions": len(submissions),
    }


def get_habit_profile(db: Session, user_id: str) -> dict:
    real_features = _compute_real_features(db, user_id)
    if real_features is None:
        return {
            "available": False,
            "reason": f"Solve at least {MIN_SUBMISSIONS_FOR_PROFILE} problems first -- not enough submission history yet for a real profile.",
        }

    clf = _get_model()
    vector = np.array([[real_features[name] for name in FEATURE_NAMES]])
    probs = clf.predict_proba(vector)[0]
    habit = clf.classes_[int(np.argmax(probs))]
    confidence = float(np.max(probs))

    return {
        "available": True,
        "habit": habit,
        "coaching_tip": HABITS[habit],
        "confidence": confidence,
        "features": real_features,
    }
