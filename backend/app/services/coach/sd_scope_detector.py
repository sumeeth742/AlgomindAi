"""
A real neural network (MLPClassifier) that reads a submitted System Design
architecture and predicts whether it's appropriately scoped for its stated
scale tier -- over-engineered, under-engineered, or well-scoped -- trained
the same way as the existing diagnosis model: on a synthetic dataset whose
labels come from an explicit rule function encoding this app's own standing
pedagogy (the critique engine's "why did you add this?" challenge already
enforces: don't add unjustified complexity at small scale, don't skip
necessary components at large scale). The trained classifier generalizes
across missing/unjustified-component COMBINATIONS the fixed rules in
critique.py don't score as a single scope verdict, complementing rather than
replacing that deterministic per-component critique.

The features fed in at prediction time are always real: the actual
missing/unjustified component counts critique_architecture() already
computes for this specific submitted architecture, never invented.
"""
from __future__ import annotations

import random
from functools import lru_cache

import numpy as np
from sklearn.neural_network import MLPClassifier

SCOPE_LABELS = {
    "OVER_ENGINEERED": "This design adds real complexity the stated scale doesn't yet need -- each unjustified component should earn its place, not be added by default.",
    "SLIGHTLY_OVER_ENGINEERED": "Mostly right-sized, but at least one component here isn't clearly justified by the scale -- make sure you can defend why it's needed.",
    "WELL_SCOPED": "The component set matches what this scale actually requires -- neither missing something necessary nor adding something premature.",
    "SLIGHTLY_UNDER_ENGINEERED": "Close, but at least one component this scale genuinely needs is missing from the design.",
    "UNDER_ENGINEERED": "This design is missing real components the stated scale needs to actually work -- revisit what breaks at this traffic/data volume without them.",
}

TIER_ORDINAL = {"startup": 0, "growth": 1, "global": 2}

FEATURE_NAMES = ["scale_tier_ordinal", "num_present", "num_missing", "num_unjustified"]


def _label_example(f: dict) -> str:
    tier = f["scale_tier_ordinal"]
    if f["num_unjustified"] >= 2:
        return "OVER_ENGINEERED"
    if f["num_unjustified"] >= 1 and tier == 0:
        # at startup scale, even one unjustified "extra" component is a bigger tell
        return "OVER_ENGINEERED"
    if f["num_missing"] >= 2:
        return "UNDER_ENGINEERED"
    if f["num_missing"] >= 1 and tier == 2:
        # at global scale, missing even one truly necessary component is a bigger gap
        return "UNDER_ENGINEERED"
    if f["num_unjustified"] == 0 and f["num_missing"] == 0:
        return "WELL_SCOPED"
    if f["num_unjustified"] >= 1:
        return "SLIGHTLY_OVER_ENGINEERED"
    return "SLIGHTLY_UNDER_ENGINEERED"


def _generate_synthetic_dataset(n: int, seed: int = 42):
    rng = random.Random(seed)
    X, y = [], []
    for _ in range(n):
        f = {
            "scale_tier_ordinal": rng.choice([0, 1, 2]),
            "num_present": rng.randint(2, 9),
            "num_missing": rng.choice([0, 0, 0, 1, 1, 2, 3]),
            "num_unjustified": rng.choice([0, 0, 0, 1, 1, 2, 3]),
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


def predict_scope(scale_tier: str | None, num_present: int, num_missing: int, num_unjustified: int) -> dict:
    clf = _get_model()
    tier_ordinal = TIER_ORDINAL.get(scale_tier or "growth", 1)
    vector = np.array([[tier_ordinal, num_present, num_missing, num_unjustified]])
    probs = clf.predict_proba(vector)[0]
    label = clf.classes_[int(np.argmax(probs))]
    confidence = float(np.max(probs))

    return {
        "scope_verdict": label,
        "coaching_tip": SCOPE_LABELS[label],
        "confidence": confidence,
    }
