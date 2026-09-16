"""
Root-cause classifier — a real scikit-learn model, not an LLM call (per the user's
explicit choice: "without api key use deeplearning and ml").

The model is trained in-process, once per server lifetime, on a synthetically
generated but rule-grounded dataset: the label for each synthetic example is
produced by `_label_example`, which encodes the same domain knowledge a human
TA would use (e.g. "used O(n^2) code against an O(n)-expected problem with a
low pass ratio and no hint use" -> TIME_COMPLEXITY). Training a classifier on
this is what lets the system report a *confidence* and generalize across
feature combinations the rules didn't explicitly enumerate, instead of being a
frozen if/elif ladder. It is never told which real user it is diagnosing.
"""
from __future__ import annotations

import random
from functools import lru_cache

import numpy as np
from sklearn.ensemble import RandomForestClassifier

CATEGORIES = [
    "MASTERED",
    "CONCEPT_GAP",
    "PATTERN_RECOGNITION",
    "IMPLEMENTATION",
    "TIME_COMPLEXITY",
    "EDGE_CASE",
    "HINT_DEPENDENCY",
]

# feature order must match diagnosis.engine.build_feature_vector
FEATURE_NAMES = [
    "passed_ratio", "hint_count_used", "attempt_number", "time_ratio",
    "loc", "max_loop_nesting", "uses_recursion", "uses_dict_or_set",
    "uses_two_index_vars", "uses_sorted_or_sort", "uses_heap",
    "has_early_return_in_loop", "expected_uses_hash", "expected_complexity_class",
    "declared_pattern_correct",
]


def _label_example(f: dict) -> str:
    if f["passed_ratio"] >= 0.999 and f["hint_count_used"] == 0 and f["attempt_number"] <= 2:
        return "MASTERED"
    if f["hint_count_used"] >= 3:
        return "HINT_DEPENDENCY"
    if f["declared_pattern_correct"] == 0 and f["passed_ratio"] < 0.6:
        return "PATTERN_RECOGNITION"
    if f["expected_complexity_class"] <= 1 and f["max_loop_nesting"] >= 2 and f["passed_ratio"] < 1.0:
        return "TIME_COMPLEXITY"
    if f["expected_uses_hash"] == 1 and f["uses_dict_or_set"] == 0 and f["passed_ratio"] < 1.0:
        return "CONCEPT_GAP"
    if 0.5 <= f["passed_ratio"] < 1.0:
        return "EDGE_CASE"
    if f["passed_ratio"] < 0.5:
        return "IMPLEMENTATION"
    return "MASTERED"


def _generate_synthetic_dataset(n: int, seed: int = 42):
    rng = random.Random(seed)
    X, y = [], []
    for _ in range(n):
        f = {
            "passed_ratio": rng.choice([0.0, 0.2, 0.4, 0.5, 0.6, 0.75, 0.9, 1.0]),
            "hint_count_used": rng.choice([0, 0, 0, 1, 2, 3, 4]),
            "attempt_number": rng.choice([1, 1, 2, 3, 4, 5]),
            "time_ratio": rng.uniform(0.2, 4.0),
            "loc": rng.randint(3, 60),
            "max_loop_nesting": rng.choice([0, 1, 1, 2, 3]),
            "uses_recursion": rng.choice([0, 1]),
            "uses_dict_or_set": rng.choice([0, 1]),
            "uses_two_index_vars": rng.choice([0, 1]),
            "uses_sorted_or_sort": rng.choice([0, 1]),
            "uses_heap": rng.choice([0, 1]),
            "has_early_return_in_loop": rng.choice([0, 1]),
            "expected_uses_hash": rng.choice([0, 1]),
            "expected_complexity_class": rng.choice([0, 1, 2, 3]),
            "declared_pattern_correct": rng.choice([0, 1, 1]),
        }
        label = _label_example(f)
        X.append([f[name] for name in FEATURE_NAMES])
        y.append(label)
    return np.array(X, dtype=float), np.array(y)


@lru_cache(maxsize=1)
def get_model() -> RandomForestClassifier:
    X, y = _generate_synthetic_dataset(n=4000)
    clf = RandomForestClassifier(n_estimators=120, max_depth=8, random_state=42)
    clf.fit(X, y)
    return clf


def predict(feature_vector: list[float]) -> tuple[str, float, dict[str, float]]:
    clf = get_model()
    probs = clf.predict_proba([feature_vector])[0]
    class_probs = dict(zip(clf.classes_, probs))
    best_label = max(class_probs, key=class_probs.get)
    return best_label, float(class_probs[best_label]), {k: float(v) for k, v in class_probs.items()}
