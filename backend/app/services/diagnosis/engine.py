"""
Diagnosis engine (spec section 50).

Combines the deterministic static-analysis features with the trained
classifier to produce a structured diagnosis. Every string in `evidence` is
generated from an actually-observed value — never invented — and if the
signal is too thin (e.g. zero prior attempts on this skill) the engine
returns INSUFFICIENT_EVIDENCE instead of guessing, per spec section 66.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.services.diagnosis import model as diagnosis_model
from app.services.diagnosis.features import CodeFeatures

RECOMMENDATION_BY_CATEGORY = {
    "MASTERED": "ADVANCE_DIFFICULTY",
    "CONCEPT_GAP": "RETURN_TO_CONCEPT_LESSON",
    "PATTERN_RECOGNITION": "RETRIEVAL_AND_PATTERN_DRILL",
    "IMPLEMENTATION": "GUIDED_REIMPLEMENTATION",
    "TIME_COMPLEXITY": "COMPLEXITY_DRILL",
    "EDGE_CASE": "EDGE_CASE_DRILL",
    "HINT_DEPENDENCY": "INDEPENDENT_RETRY_WITHOUT_HINTS",
}


@dataclass
class Diagnosis:
    primary_issue: str
    skill_key: str
    confidence: float
    evidence: list[str]
    recommendation: str
    class_probabilities: dict[str, float]


def diagnose(
    *,
    skill_key: str,
    passed_count: int,
    total_count: int,
    hint_count_used: int,
    attempt_number: int,
    time_to_solve_seconds: float | None,
    expected_time_seconds: float,
    code_features: CodeFeatures,
    expected_uses_hash: bool,
    expected_complexity_class: int,
    declared_pattern_correct: bool | None,
) -> Diagnosis | None:
    if total_count == 0:
        return None  # INSUFFICIENT_EVIDENCE: no tests were actually run

    passed_ratio = passed_count / total_count
    time_ratio = (time_to_solve_seconds / expected_time_seconds) if (time_to_solve_seconds and expected_time_seconds) else 1.0

    feature_vector = [
        passed_ratio,
        hint_count_used,
        attempt_number,
        time_ratio,
        code_features.loc,
        code_features.max_loop_nesting,
        float(code_features.uses_recursion),
        float(code_features.uses_dict_or_set),
        float(code_features.uses_two_index_vars),
        float(code_features.uses_sorted_or_sort),
        float(code_features.uses_heap),
        float(code_features.has_early_return_in_loop),
        float(expected_uses_hash),
        expected_complexity_class,
        1.0 if declared_pattern_correct in (True, None) else 0.0,
    ]

    label, confidence, class_probs = diagnosis_model.predict(feature_vector)

    evidence = [f"{passed_count}/{total_count} visible+hidden tests passed"]
    if hint_count_used:
        evidence.append(f"Used {hint_count_used} hint(s) before this submission")
    if attempt_number > 1:
        evidence.append(f"This was attempt #{attempt_number} on this problem")
    if code_features.max_loop_nesting >= 2 and expected_complexity_class <= 1:
        evidence.append(f"Code has {code_features.max_loop_nesting} nested loops; problem constraints favor a linear/near-linear solution")
    if expected_uses_hash and not code_features.uses_dict_or_set:
        evidence.append("Problem's expected pattern uses hashing (dict/set), but submission uses neither")
    if declared_pattern_correct is False:
        evidence.append("Declared pattern before coding did not match the problem's intended pattern")
    if time_ratio > 1.5:
        evidence.append(f"Took {time_ratio:.1f}x the expected time for this difficulty")

    return Diagnosis(
        primary_issue=label,
        skill_key=skill_key,
        confidence=round(confidence, 3),
        evidence=evidence,
        recommendation=RECOMMENDATION_BY_CATEGORY.get(label, "REVIEW_CONCEPT"),
        class_probabilities={k: round(v, 3) for k, v in class_probs.items()},
    )


def detect_brute_force(code_features: CodeFeatures, expected_complexity_class: int, expected_complexity_label: str) -> str | None:
    """Deterministic and always-on -- unlike the ML diagnosis above, this never gets
    suppressed by a 'MASTERED' classification. The classifier was trained to treat a
    high pass rate as evidence of mastery (reasonably, most of the time), which means
    it systematically stays quiet about a nested-loop solution that happens to pass
    anyway because the hidden test cases weren't large enough to expose it. This
    check exists specifically to catch that case: passing tests is not the same as
    having found the intended approach, and staying silent about it would let a
    learner reinforce brute-force habits every time small inputs let them get away
    with it."""
    if expected_complexity_class <= 1 and code_features.max_loop_nesting >= 2:
        return (
            f"This passed, but the code has {code_features.max_loop_nesting} nested loops -- that's usually an "
            f"O(n^2)-or-worse shape. This problem is solvable in {expected_complexity_label}. Small test cases often "
            "let a brute-force solution pass anyway, but a larger input would time out. Try to find the approach "
            "that avoids the nested loop before moving on."
        )
    return None
