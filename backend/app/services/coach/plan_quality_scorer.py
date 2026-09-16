"""
A real neural network (MLPClassifier) that scores the QUALITY of a student's
stated plan/reasoning -- written before they see any code -- trained the
same way as the existing diagnosis model: on a synthetic dataset whose
labels come from an explicit rule function encoding real TA judgment (does
this reasoning actually show complexity awareness and consideration of
alternatives, or is it a correct-pattern guess with no real justification).

The training labels are synthetic-but-rule-grounded; the FEATURES are always
extracted for real from the student's actual submitted reasoning_text via
deterministic regex/keyword checks -- never a semantic judgment invented by
a model that doesn't actually understand the text, which is exactly why this
uses structural text features (does it mention complexity notation, does it
discuss an alternative approach) rather than pretending to grade meaning.
"""
from __future__ import annotations

import random
import re
from functools import lru_cache

import numpy as np
from sklearn.neural_network import MLPClassifier

TRADEOFF_WORDS = ("instead", "however", "but ", "tradeoff", "trade-off", "alternative", "brute force", "naive", "rather than")
EDGE_CASE_WORDS = ("edge case", "empty", "null", "boundary", "duplicate")
COMPLEXITY_PATTERN = re.compile(r"o\(\s*[\w\s\^\*\+log]+\)", re.IGNORECASE)

PLAN_TIERS = {
    "STRONG": "Real reasoning -- names the pattern, shows complexity awareness, and considers an alternative approach. This is exactly the habit that separates strong interview answers.",
    "ADEQUATE": "The right pattern, stated plainly -- try going one step further next time: name the expected complexity, or explain why a simpler approach wouldn't work.",
    "WEAK": "Too little here to show real reasoning happened before coding -- try writing 2-3 sentences: what pattern, why, and roughly what complexity you expect.",
}

FEATURE_NAMES = ["word_count", "has_complexity_notation", "mentions_tradeoff", "mentions_edge_case", "matched_evidence_count", "declared_pattern_correct"]


def _extract_text_features(reasoning_text: str, matched_evidence_count: int, declared_pattern_correct: bool) -> dict:
    text = reasoning_text.lower()
    return {
        "word_count": len(reasoning_text.split()),
        "has_complexity_notation": bool(COMPLEXITY_PATTERN.search(reasoning_text)),
        "mentions_tradeoff": any(w in text for w in TRADEOFF_WORDS),
        "mentions_edge_case": any(w in text for w in EDGE_CASE_WORDS),
        "matched_evidence_count": matched_evidence_count,
        "declared_pattern_correct": declared_pattern_correct,
    }


def _label_example(f: dict) -> str:
    if f["word_count"] < 5:
        return "WEAK"
    if not f["declared_pattern_correct"]:
        return "WEAK"
    if f["has_complexity_notation"] and (f["matched_evidence_count"] >= 2 or f["mentions_tradeoff"]):
        return "STRONG"
    return "ADEQUATE"


def _generate_synthetic_dataset(n: int, seed: int = 42):
    rng = random.Random(seed)
    X, y = [], []
    for _ in range(n):
        f = {
            "word_count": rng.choice([0, 2, 4, 8, 15, 25, 40]),
            "has_complexity_notation": rng.choice([0, 1]),
            "mentions_tradeoff": rng.choice([0, 1]),
            "mentions_edge_case": rng.choice([0, 1]),
            "matched_evidence_count": rng.choice([0, 1, 2, 3, 4]),
            "declared_pattern_correct": rng.choice([0, 1, 1]),
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


def score_plan_quality(reasoning_text: str, matched_evidence_count: int, declared_pattern_correct: bool) -> dict:
    clf = _get_model()
    real_features = _extract_text_features(reasoning_text, matched_evidence_count, declared_pattern_correct)
    vector = np.array([[float(real_features[name]) for name in FEATURE_NAMES]])
    probs = clf.predict_proba(vector)[0]
    tier = clf.classes_[int(np.argmax(probs))]
    confidence = float(np.max(probs))

    return {
        "plan_quality_tier": tier,
        "coaching_tip": PLAN_TIERS[tier],
        "confidence": confidence,
    }
