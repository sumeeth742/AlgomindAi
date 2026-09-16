"""
Rule-based critique for low-level (class-based) design exercises -- the LLD
counterpart to critique.py's critique_architecture(). Deliberately not an
LLM: matching submitted class names against a case's own expected_classes
list (by name or a declared alias, never penalizing a reasonable synonym),
checking for real inheritance/interface usage, and flagging classes with an
unusually large number of methods (a real, if rough, Single Responsibility
signal) are all deterministic checks grounded in what the learner actually
submitted -- never a model's opinion of "good design."
"""
from __future__ import annotations

GOD_CLASS_METHOD_THRESHOLD = 8


def critique_lld_design(classes: list[dict], expected_classes: list[dict]) -> dict:
    submitted_names = {c["name"].strip().lower() for c in classes if c.get("name")}

    missing = []
    for exp in expected_classes:
        aliases = {exp["name"].lower()} | {a.lower() for a in exp.get("aliases", [])}
        if not (aliases & submitted_names):
            missing.append(exp["name"])

    known_names = {exp["name"].lower() for exp in expected_classes}
    known_names |= {a.lower() for exp in expected_classes for a in exp.get("aliases", [])}
    extra = [c["name"] for c in classes if c.get("name") and c["name"].strip().lower() not in known_names]

    uses_abstraction = any(c.get("extends") or c.get("implements") for c in classes)

    god_classes = [
        c["name"] for c in classes
        if c.get("name") and len(c.get("methods") or []) > GOD_CLASS_METHOD_THRESHOLD
    ]

    total_expected = max(1, len(expected_classes))
    coverage = (total_expected - len(missing)) / total_expected
    penalty = 0.1 * len(god_classes)
    score = max(0.0, min(1.0, coverage - penalty))

    why_questions = []
    if extra:
        why_questions.append(
            f"Why did you add {', '.join(extra)}? What responsibility does it hold that isn't already covered "
            "by another class?"
        )
    if god_classes:
        why_questions.append(
            f"{', '.join(god_classes)} has quite a few methods -- does it have more than one reason to change? "
            "(Single Responsibility)"
        )

    return {
        "score": round(score, 3),
        "missing_classes": missing,
        "extra_classes": extra,
        "uses_abstraction": uses_abstraction,
        "god_classes": god_classes,
        "why_questions": why_questions,
    }
