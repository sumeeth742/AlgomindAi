"""
Rule-based architecture critique + estimation grading (spec sections 48, 75).

Deliberately not an LLM: the "why did you add this?" challenge is generated
from a fixed rule table (component -> justification question), and estimation
grading is a numeric tolerance check against the case's stored expected
values. This is honest, deterministic feedback rather than a model
hallucinating a plausible-sounding critique.
"""
from __future__ import annotations

WHY_QUESTIONS = {
    "cache": "Why did you add a cache here? What specifically would be slow or expensive without it?",
    "queue": "Why is this asynchronous? What breaks if the producer called the consumer directly?",
    "load_balancer": "What happens if you only had one server instead? At what traffic level does that stop working?",
    "cdn": "What kind of content justifies a CDN here, and where are your users located?",
    "object_storage": "Why not store this in the primary database?",
    "search": "Why does this need a dedicated search index instead of a database query?",
}

def critique_architecture(nodes: list[dict], edges: list[dict], expected_components: list[str]) -> dict:
    present_types = [n["type"] for n in nodes]
    present_set = set(present_types)

    missing = [c for c in expected_components if c not in present_set]

    # Any component not on the case's expected list gets challenged, regardless of
    # graph size -- "good system design is not about adding more boxes" (spec section 75).
    unjustified = [t for t in present_types if t in WHY_QUESTIONS and t not in expected_components]

    connected_ids = {e["source"] for e in edges} | {e["target"] for e in edges}
    isolated = [n["id"] for n in nodes if n["id"] not in connected_ids and len(nodes) > 1]

    why_questions = [WHY_QUESTIONS[t] for t in present_set if t in WHY_QUESTIONS]

    total_expected = max(1, len(expected_components))
    coverage = (total_expected - len(missing)) / total_expected
    penalty = 0.1 * len(unjustified) + 0.1 * len(isolated)
    score = max(0.0, min(1.0, coverage - penalty))

    return {
        "score": round(score, 3),
        "missing_components": missing,
        "unjustified_components": unjustified,
        "isolated_nodes": isolated,
        "why_questions": why_questions,
    }


def grade_estimation(answers: dict, expected: dict, tolerance: float = 0.5) -> dict:
    """expected: {field: {"value": number, "unit": str}}. tolerance is a relative
    band (0.5 = within 50% of the expected order of magnitude) since estimation
    interviews grade reasoning, not exact numbers."""
    feedback = {}
    for field, spec in expected.items():
        target = spec["value"]
        submitted = answers.get(field)
        if submitted is None:
            feedback[field] = {"status": "missing", "expected_order_of_magnitude": target, "unit": spec.get("unit", "")}
            continue
        lower, upper = target * (1 - tolerance), target * (1 + tolerance)
        within = lower <= submitted <= upper
        feedback[field] = {
            "status": "reasonable" if within else "off",
            "submitted": submitted,
            "expected_order_of_magnitude": target,
            "unit": spec.get("unit", ""),
        }
    return feedback
