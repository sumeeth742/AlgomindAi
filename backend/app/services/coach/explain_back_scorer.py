"""
"Explain it back" (Feynman technique) scoring -- after reading a lesson, a
student writes a short explanation of the concept in their own words, and
this scores it against the lesson's own real key vocabulary (extracted from
its "## Key takeaway" section, never invented) plus structural signals
(does the explanation give a concrete example, does it explain WHY, not
just restate the name of the concept).

Same architecture and honesty split as plan_quality_scorer.py: a real
neural network (MLPClassifier) trained on a synthetic dataset whose labels
come from an explicit rule function, letting it generalize across feature
combinations the rules didn't explicitly enumerate -- but the FEATURES
themselves are always extracted for real from the student's actual
submitted text and the lesson's actual real content, never fabricated.
"""
from __future__ import annotations

import random
import re
from functools import lru_cache

import numpy as np
from sklearn.neural_network import MLPClassifier

EXAMPLE_WORDS = ("example", "like", "such as", "for instance", "e.g", "imagine", "say you")
WHY_WORDS = ("because", "since", "so that", "this means", "the reason", "which lets", "which means")
STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "of", "to", "in", "on", "for",
    "and", "or", "but", "with", "as", "that", "this", "it", "its", "at", "by", "from", "not",
    "than", "then", "so", "if", "when", "which", "what", "how", "why", "into", "over", "each",
}

QUALITY_TIERS = {
    "STRONG": "Real understanding shown here -- you used the concept's own key ideas in your own words, with an example or a reason, not just a restated definition.",
    "ADEQUATE": "You've got the gist -- try going one step further: add a concrete example, or explain WHY it works that way, not just what it's called.",
    "WEAK": "Too short/vague to show real understanding yet -- try writing 2-3 sentences using your own words, ideally with an example.",
}

FEATURE_NAMES = ["word_count", "matched_term_ratio", "mentions_example", "mentions_why"]


def _extract_key_takeaway(markdown: str) -> str:
    match = re.search(r"##\s*key takeaway\s*\n(.+?)(?=\n##|\Z)", markdown, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fall back to the "What is it?" section if there's no Key Takeaway heading.
    match = re.search(r"##\s*what is it\??\s*\n(.+?)(?=\n##|\Z)", markdown, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else markdown[:400]


def _extract_key_terms(title: str, key_takeaway: str) -> set[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", f"{title} {key_takeaway}".lower())
    return {w for w in words if w not in STOPWORDS}


def _label_example(f: dict) -> str:
    if f["word_count"] < 6:
        return "WEAK"
    if f["matched_term_ratio"] < 0.08:
        return "WEAK"
    if f["matched_term_ratio"] >= 0.18 and (f["mentions_example"] or f["mentions_why"]):
        return "STRONG"
    return "ADEQUATE"


def _generate_synthetic_dataset(n: int, seed: int = 42):
    rng = random.Random(seed)
    X, y = [], []
    for _ in range(n):
        f = {
            "word_count": rng.choice([0, 3, 6, 12, 20, 35, 60]),
            "matched_term_ratio": rng.uniform(0.0, 0.6),
            "mentions_example": rng.choice([0, 1]),
            "mentions_why": rng.choice([0, 1]),
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


def score_explanation(title: str, content_markdown: str, user_explanation: str) -> dict:
    key_takeaway = _extract_key_takeaway(content_markdown)
    key_terms = _extract_key_terms(title, key_takeaway)

    user_words = set(re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", user_explanation.lower())) - STOPWORDS
    matched = sorted(key_terms & user_words)
    matched_ratio = len(matched) / max(1, len(key_terms))

    text_lower = user_explanation.lower()
    real_features = {
        "word_count": len(user_explanation.split()),
        "matched_term_ratio": matched_ratio,
        "mentions_example": float(any(w in text_lower for w in EXAMPLE_WORDS)),
        "mentions_why": float(any(w in text_lower for w in WHY_WORDS)),
    }

    clf = _get_model()
    vector = np.array([[real_features[name] for name in FEATURE_NAMES]])
    probs = clf.predict_proba(vector)[0]
    tier = clf.classes_[int(np.argmax(probs))]
    confidence = float(np.max(probs))

    return {
        "quality_tier": tier,
        "coaching_tip": QUALITY_TIERS[tier],
        "confidence": confidence,
        "matched_terms": matched[:8],
    }
