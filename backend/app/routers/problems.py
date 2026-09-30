import random
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.problem import Hint, HintUsage, Problem, ProblemTestCase
from app.models.retention import LearningEvent
from app.models.skill import Skill
from app.models.submission import ReasoningAttempt, Submission, SubmissionStatus
from app.models.user import User
from app.schemas.problem import (
    AskRequest, AskResponse, BlindPracticeOut, ComplexityCheckRequest, ComplexityCheckResponse,
    ComplexitySampleOut, ExplainResponse, ProblemDetail, ProblemListItem,
    ReasoningSubmitRequest, ReasoningSubmitResponse, RunRequest, RunResponse,
    SubmissionHistoryItem, SubmitRequest, SubmitResponse, TestResultOut, TraceRequest, TraceResponse,
    TraceStepOut, VisibleTestCase,
)
from app.services.diagnosis.engine import detect_brute_force, diagnose
from app.services.diagnosis.features import analyze_code
from app.services.diagnosis.features_java import analyze_java_code
from app.services.diagnosis.features_js import analyze_js_code
from app.services.execution.comparison import outputs_match
from app.services.execution.complexity_probe import measure_empirical_complexity
from app.services.execution.java_sandbox import java_types_for
from app.services.execution.trace_probe import trace_java_execution, trace_javascript_execution, trace_python_execution
from app.services.execution.sandbox import run_submission
from app.services.execution.starter_code import (
    SUPPORTED_LANGUAGES, extract_param_names, function_name_for_language, generate_java_starter,
    generate_javascript_starter, infer_param_tags, infer_return_tag,
)
from app.services.coach.plan_quality_scorer import score_plan_quality
from app.services.llm.local_llm import LocalLLMUnavailable, generate as llm_generate
from app.services.retention.scheduler import get_or_create_review
from app.services.skill_graph.graph import (
    update_mastery_from_submission, update_pattern_recognition, update_transfer,
)

router = APIRouter(prefix="/problems", tags=["problems"])

COMPLEXITY_CLASS = {"O(1)": 0, "O(log n)": 0, "O(n)": 1, "O(n log n)": 1, "O(n^2)": 2, "O(2^n)": 3, "O(n!)": 3}


def _param_and_return_tags(problem: Problem):
    """Infers one TypeTag per parameter and for the return value from the
    problem's own (already reference-executed) test-case data -- see
    starter_code.py's module docstring for why this is derived rather than
    hand-authored per language."""
    all_args = [tc.args for tc in problem.test_cases]
    all_outputs = [tc.expected_output for tc in problem.test_cases]
    param_tags = infer_param_tags(all_args, problem.io_transform)
    return_tag = infer_return_tag(all_outputs, problem.io_transform)
    return param_tags, return_tag


def _starter_code_for(problem: Problem, language: str) -> str:
    if language == "python":
        return problem.starter_code_python
    param_names = extract_param_names(problem.starter_code_python, problem.function_name)
    param_tags, return_tag = _param_and_return_tags(problem)
    if language == "javascript":
        return generate_javascript_starter(problem.function_name, param_names, param_tags, return_tag, problem.io_transform)
    if language == "java":
        return generate_java_starter(problem.function_name, param_names, param_tags, return_tag)
    raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")


def _analyze_submission(code: str, call_name: str, language: str):
    """Dispatches to the right language's static analyzer -- see
    diagnosis/features.py (Python, ast), features_java.py (javalang, a real
    Java parser), and features_js.py (espree, a real JS parser) for how each
    one is computed. All three return the same CodeFeatures shape so the
    diagnosis model and detect_brute_force() don't need to know or care which
    language produced them."""
    if language == "java":
        return analyze_java_code(code, call_name)
    if language == "javascript":
        return analyze_js_code(code, call_name)
    return analyze_code(code, call_name)


def _java_call_types(problem: Problem) -> tuple[list[str], str]:
    param_tags, return_tag = _param_and_return_tags(problem)
    return java_types_for(param_tags, return_tag)


def _runtime_percentile(db: Session, problem_id: str, language: str, this_runtime_ms: float) -> float | None:
    """What fraction of every real PASSED submission for this problem, in this
    same language, across every user, ran no faster than this one -- computed
    fresh from actual Submission rows every time, never a fabricated or
    canned number. Withheld (None) until there's a real comparison pool,
    since "beats 100% of 1 submission" is not a meaningful stat."""
    runtimes = [
        r[0] for r in db.query(Submission.runtime_ms).filter(
            Submission.problem_id == problem_id, Submission.language == language,
            Submission.status == SubmissionStatus.passed,
        ).all()
    ]
    if len(runtimes) < 4:
        return None
    no_faster = sum(1 for r in runtimes if r >= this_runtime_ms)
    return round(100 * no_faster / len(runtimes), 1)


@router.get("", response_model=list[ProblemListItem])
def list_problems(
    skill: str | None = None, difficulty: str | None = None,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    q = db.query(Problem)
    if skill:
        q = q.join(Skill, Problem.primary_skill_id == Skill.id).filter(Skill.key == skill)
    if difficulty:
        q = q.filter(Problem.difficulty == difficulty)
    problems = q.all()

    user_submissions = db.query(Submission).filter(Submission.user_id == current_user.id).all()
    solved_ids = {s.problem_id for s in user_submissions if s.status.value == "PASSED"}
    attempted_ids = {s.problem_id for s in user_submissions}

    out = []
    for p in problems:
        out.append(ProblemListItem(
            id=p.id, slug=p.slug, title=p.title, difficulty=p.difficulty.value,
            primary_skill_key=p.primary_skill.key,
            concept_difficulty=p.concept_difficulty, implementation_difficulty=p.implementation_difficulty,
            reasoning_difficulty=p.reasoning_difficulty, pattern_difficulty=p.pattern_difficulty,
            solved=p.id in solved_ids, attempted=p.id in attempted_ids,
        ))
    return out


@router.get("/blind/random", response_model=BlindPracticeOut)
def blind_practice_pick(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Picks a random problem with no skill/chapter context revealed anywhere in the
    surrounding page -- the point is forcing genuinely unprompted pattern recognition
    instead of recognizing a pattern because you just clicked into its chapter. Prefers
    problems the user hasn't solved yet; falls back to any problem once everything is solved."""
    all_ids = [p.id for p in db.query(Problem.id).all()]
    if not all_ids:
        return BlindPracticeOut(available=False, reason="No problems are seeded yet.")

    solved_ids = {
        s.problem_id for s in db.query(Submission).filter(
            Submission.user_id == current_user.id, Submission.status == SubmissionStatus.passed,
        ).all()
    }
    unsolved_ids = [pid for pid in all_ids if pid not in solved_ids]
    pool = unsolved_ids or all_ids
    chosen = db.query(Problem).filter(Problem.id == random.choice(pool)).first()

    reason = (
        "Randomly selected from problems you haven't solved yet -- no skill or chapter hint attached."
        if unsolved_ids else
        "You've solved every seeded problem at least once, so this is a random repeat -- great problem to try in Transfer mode instead."
    )
    return BlindPracticeOut(available=True, problem_slug=chosen.slug, reason=reason)


@router.get("/{slug}", response_model=ProblemDetail)
def get_problem(slug: str, mode: str = "standard", language: str = "python", db: Session = Depends(get_db)):
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    visible = [
        VisibleTestCase(args=tc.args, expected_output=tc.expected_output, explanation=tc.explanation)
        for tc in problem.test_cases if not tc.is_hidden
    ]
    return ProblemDetail(
        id=problem.id, slug=problem.slug, title=problem.title,
        statement_markdown=problem.statement_markdown, difficulty=problem.difficulty.value,
        constraints_markdown=problem.constraints_markdown, examples=problem.examples,
        function_name=problem.function_name,
        param_names=extract_param_names(problem.starter_code_python, problem.function_name),
        starter_code=_starter_code_for(problem, language),
        language=language, supported_languages=SUPPORTED_LANGUAGES,
        time_limit_ms=problem.time_limit_ms, expected_complexity=problem.expected_complexity,
        primary_skill_key="" if mode == "blind" else problem.primary_skill.key,
        visible_test_cases=visible,
    )


@router.get("/{slug}/hints/{level}")
def get_hint(slug: str, level: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    hint = db.query(Hint).filter(Hint.problem_id == problem.id, Hint.level == level).first()
    if not hint:
        raise HTTPException(status_code=404, detail="No hint at this level")
    db.add(HintUsage(user_id=current_user.id, problem_id=problem.id, hint_id=hint.id))
    db.commit()
    return {"level": level, "text_markdown": hint.text_markdown}


@router.post("/{slug}/reasoning", response_model=ReasoningSubmitResponse)
def submit_reasoning(
    slug: str, payload: ReasoningSubmitRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    correct_patterns = set(problem.pattern_skill_ids or [problem.primary_skill.key])
    is_correct = payload.declared_pattern in correct_patterns

    # evidence-overlap based quality score: how many correctness-relevant keywords
    # (drawn from the skill's own name/description, not invented) appear in the reasoning
    corpus_terms = set()
    for skill_key in correct_patterns:
        skill = db.query(Skill).filter(Skill.key == skill_key).first()
        if skill:
            corpus_terms.update(w.lower() for w in (skill.name + " " + skill.description).split())
    reasoning_terms = set(w.lower().strip(".,") for w in payload.reasoning_text.split())
    matched = sorted(corpus_terms & reasoning_terms)
    quality = min(1.0, len(matched) / 3) if matched or payload.reasoning_text else 0.0

    # Reasoning gap diff: when the declared pattern is wrong, show WHICH real
    # signal from the correct pattern's own vocabulary is genuinely missing
    # from the reasoning text (not just how many matched), and -- if the
    # declared pattern is itself a real skill -- which of ITS real vocabulary
    # the reasoning text actually used, so a learner sees exactly why their
    # reasoning read as the wrong pattern instead of just being told it was
    # wrong. Both sides come from the same skill name/description corpus
    # already used for `matched`, never invented text.
    missing_evidence = sorted(w for w in (corpus_terms - reasoning_terms) if len(w) >= 3)[:8]
    declared_pattern_evidence: list[str] = []
    if not is_correct:
        declared_skill = db.query(Skill).filter(Skill.key == payload.declared_pattern).first()
        if declared_skill:
            declared_terms = set(w.lower() for w in (declared_skill.name + " " + declared_skill.description).split())
            declared_pattern_evidence = sorted(w for w in (declared_terms & reasoning_terms) if len(w) >= 3)

    attempt = ReasoningAttempt(
        user_id=current_user.id, problem_id=problem.id, declared_pattern=payload.declared_pattern,
        reasoning_text=payload.reasoning_text, is_correct_pattern=is_correct,
        reasoning_quality_score=quality, evidence_matched=matched,
    )
    db.add(attempt)
    update_pattern_recognition(db, current_user.id, problem.primary_skill_id, is_correct)
    db.commit()

    feedback = (
        "Correct pattern identified before writing any code -- that's the skill that matters most."
        if is_correct else
        f"The intended pattern here is {problem.primary_skill.key}. Review why the clues point there before coding."
    )
    plan_quality_coach = score_plan_quality(payload.reasoning_text, len(matched), is_correct)
    return ReasoningSubmitResponse(
        is_correct_pattern=is_correct, correct_pattern=problem.primary_skill.key,
        reasoning_quality_score=quality, evidence_matched=matched,
        missing_evidence=missing_evidence, declared_pattern_evidence=declared_pattern_evidence,
        feedback=feedback, plan_quality_coach=plan_quality_coach,
    )


@router.post("/{slug}/run", response_model=RunResponse)
def run_against_visible_tests(
    slug: str, payload: RunRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Like a real IDE's 'Run' button: executes against the *visible* example tests
    only, for fast iteration. Unlike /submit, this never creates a Submission row,
    never touches skill mastery/retention, and never triggers diagnosis -- it's
    scratch space, not an attempt that counts."""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    if payload.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {payload.language}")

    java_param_types, java_return_type = (
        _java_call_types(problem) if payload.language == "java" else (None, None)
    )
    visible_cases = [tc for tc in problem.test_cases if not tc.is_hidden]
    call_name = function_name_for_language(problem.function_name, payload.language)
    exec_result = run_submission(
        payload.code, call_name, [tc.args for tc in visible_cases], problem.io_transform,
        language=payload.language, java_param_types=java_param_types, java_return_type=java_return_type,
    )

    test_results: list[TestResultOut] = []
    passed_count = 0
    if exec_result.status in ("TIMEOUT", "RUNTIME_ERROR", "COMPILE_ERROR"):
        status_value = exec_result.status
        for i, tc in enumerate(visible_cases):
            test_results.append(TestResultOut(
                index=i, passed=False, is_hidden=False, input=tc.args, expected=tc.expected_output,
                error=exec_result.error_message,
            ))
    else:
        for i, (tc, outcome) in enumerate(zip(visible_cases, exec_result.outcomes)):
            passed = outcome.kind == "ok" and outputs_match(outcome.value, tc.expected_output, problem.output_comparison)
            if passed:
                passed_count += 1
            test_results.append(TestResultOut(
                index=i, passed=passed, is_hidden=False, input=tc.args, expected=tc.expected_output,
                actual=outcome.value, error=outcome.message if outcome.kind == "runtime_error" else None,
            ))
        status_value = "PASSED" if passed_count == len(visible_cases) and visible_cases else "FAILED"

    return RunResponse(
        status=status_value, passed_count=passed_count, total_count=len(visible_cases),
        runtime_ms=exec_result.runtime_ms, test_results=test_results,
    )


@router.post("/{slug}/submit", response_model=SubmitResponse)
def submit_solution(
    slug: str, payload: SubmitRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    if payload.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {payload.language}")

    java_param_types, java_return_type = (
        _java_call_types(problem) if payload.language == "java" else (None, None)
    )
    test_cases: list[ProblemTestCase] = problem.test_cases
    call_name = function_name_for_language(problem.function_name, payload.language)
    exec_result = run_submission(
        payload.code, call_name, [tc.args for tc in test_cases], problem.io_transform,
        language=payload.language, java_param_types=java_param_types, java_return_type=java_return_type,
    )

    test_results: list[TestResultOut] = []
    passed_count = 0

    if exec_result.status in ("TIMEOUT", "RUNTIME_ERROR", "COMPILE_ERROR"):
        status_value = exec_result.status
        for i, tc in enumerate(test_cases):
            test_results.append(TestResultOut(
                index=i, passed=False, is_hidden=tc.is_hidden,
                input=None if tc.is_hidden else tc.args,
                expected=None if tc.is_hidden else tc.expected_output,
                error=exec_result.error_message if not tc.is_hidden else None,
            ))
    else:
        for i, (tc, outcome) in enumerate(zip(test_cases, exec_result.outcomes)):
            passed = outcome.kind == "ok" and outputs_match(outcome.value, tc.expected_output, problem.output_comparison)
            if passed:
                passed_count += 1
            test_results.append(TestResultOut(
                index=i, passed=passed, is_hidden=tc.is_hidden,
                input=None if tc.is_hidden else tc.args,
                expected=None if tc.is_hidden else tc.expected_output,
                actual=None if tc.is_hidden else outcome.value,
                error=outcome.message if outcome.kind == "runtime_error" else None,
            ))
        status_value = "PASSED" if passed_count == len(test_cases) and test_cases else "FAILED"

    attempt_number = db.query(Submission).filter(
        Submission.user_id == current_user.id, Submission.problem_id == problem.id
    ).count() + 1
    already_passed_before = db.query(Submission).filter(
        Submission.user_id == current_user.id, Submission.problem_id == problem.id,
        Submission.status == SubmissionStatus.passed,
    ).first() is not None

    submission = Submission(
        user_id=current_user.id, problem_id=problem.id, mode=payload.mode, language=payload.language, code=payload.code,
        status=status_value, passed_count=passed_count, total_count=len(test_cases),
        runtime_ms=exec_result.runtime_ms,
        test_results=[t.model_dump() for t in test_results],
        error_message=exec_result.error_message,
        hint_count_used=payload.hint_count_used, time_to_solve_seconds=payload.time_to_solve_seconds,
        attempt_number=attempt_number,
    )
    db.add(submission)

    correct = status_value == "PASSED"
    updated_us = update_mastery_from_submission(
        db, current_user.id, problem.primary_skill_id, correct=correct, difficulty=problem.difficulty.value,
        is_repeat_solve=already_passed_before,
    )
    if payload.mode == "transfer":
        update_transfer(db, current_user.id, problem.primary_skill_id, correct)

    review = get_or_create_review(db, current_user.id, problem.primary_skill_id)
    if correct and review.repetitions == 0 and review.last_reviewed_at is None:
        review.due_at = datetime.utcnow()  # newly-touched skill enters the retention queue immediately

    db.add(LearningEvent(
        user_id=current_user.id, event_type="SUBMISSION", skill_id=problem.primary_skill_id,
        problem_id=problem.id, payload={"status": status_value, "mode": payload.mode},
    ))

    diagnosis_out = None
    optimization_nudge = None
    if status_value in ("FAILED", "PASSED") and test_cases:
        code_features = _analyze_submission(payload.code, call_name, payload.language)
        expected_complexity_class = COMPLEXITY_CLASS.get(problem.expected_complexity, 1)
        if status_value == "PASSED":
            optimization_nudge = detect_brute_force(code_features, expected_complexity_class, problem.expected_complexity)
        last_reasoning = (
            db.query(ReasoningAttempt)
            .filter(ReasoningAttempt.user_id == current_user.id, ReasoningAttempt.problem_id == problem.id)
            .order_by(ReasoningAttempt.created_at.desc()).first()
        )
        diag = diagnose(
            skill_key=problem.primary_skill.key, passed_count=passed_count, total_count=len(test_cases),
            hint_count_used=payload.hint_count_used, attempt_number=attempt_number,
            time_to_solve_seconds=payload.time_to_solve_seconds,
            expected_time_seconds={"easy": 600, "medium": 1200, "hard": 2100, "expert": 3000}.get(problem.difficulty.value, 1200),
            code_features=code_features,
            expected_uses_hash="HASHING" in (problem.pattern_skill_ids or []) or problem.primary_skill.key == "HASHING",
            expected_complexity_class=expected_complexity_class,
            declared_pattern_correct=last_reasoning.is_correct_pattern if last_reasoning else None,
        )
        if diag:
            diagnosis_out = {
                "primary_issue": diag.primary_issue, "confidence": diag.confidence,
                "evidence": diag.evidence, "recommendation": diag.recommendation,
            }
            submission.diagnosis = diagnosis_out

    db.commit()

    repeat_note = None
    if already_passed_before and correct:
        repeat_note = (
            "You'd already solved this one -- re-solving it barely moves mastery, since it mostly measures "
            "whether you remembered your own last solution. Try a new problem or the skill's Transfer Challenge "
            "to actually demonstrate growth."
        )

    runtime_percentile = _runtime_percentile(db, problem.id, payload.language, exec_result.runtime_ms) if correct else None

    return SubmitResponse(
        submission_id=submission.id, status=status_value, passed_count=passed_count,
        total_count=len(test_cases), runtime_ms=exec_result.runtime_ms, test_results=test_results,
        diagnosis=diagnosis_out, updated_mastery=updated_us.mastery, repeat_solve_note=repeat_note,
        optimization_nudge=optimization_nudge, language=payload.language, runtime_percentile=runtime_percentile,
    )


@router.get("/{slug}/submissions", response_model=list[SubmissionHistoryItem])
def list_my_submissions(
    slug: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    subs = (
        db.query(Submission)
        .filter(Submission.user_id == current_user.id, Submission.problem_id == problem.id)
        .order_by(Submission.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        SubmissionHistoryItem(
            id=s.id, status=s.status.value, language=s.language or "python",
            passed_count=s.passed_count, total_count=s.total_count, runtime_ms=s.runtime_ms,
            created_at=s.created_at, code=s.code,
        )
        for s in subs
    ]


@router.post("/{slug}/verify-complexity", response_model=ComplexityCheckResponse)
def verify_complexity(
    slug: str, payload: ComplexityCheckRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Opt-in, separate from /submit on purpose: re-running a solution at
    several larger synthetic sizes to measure real scaling takes real extra
    seconds (up to ~20s worst case across 4 sizes), so it's a deliberate
    follow-up action after solving, not something added to every submit."""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    param_tags, _ = _param_and_return_tags(problem)
    test_case_args = [tc.args for tc in problem.test_cases]
    report = measure_empirical_complexity(
        payload.code, function_name_for_language(problem.function_name, payload.language), payload.language,
        test_case_args, param_tags, problem.io_transform, problem.expected_complexity,
    )
    return ComplexityCheckResponse(
        supported=report.supported, reason=report.reason,
        samples=[ComplexitySampleOut(size=s.size, status=s.status, runtime_ms=s.runtime_ms) for s in report.samples],
        estimated_exponent=report.estimated_exponent, estimated_label=report.estimated_label,
        expected_complexity=problem.expected_complexity, likely_matches_expected=report.likely_matches_expected,
        explanation=report.explanation,
    )


@router.post("/{slug}/trace", response_model=TraceResponse)
def trace_execution(
    slug: str, payload: TraceRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Steps through the learner's OWN code on one specific input, instead of
    the reference solution -- see trace_probe.py. `args` must exactly match a
    VISIBLE example test case; this is deliberately not "trace any input you
    like" so it can't be used as a side channel to probe a hidden test case's
    input by trial and error."""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    if payload.language not in SUPPORTED_LANGUAGES:
        return TraceResponse(supported=False, reason=f"Step-through tracing isn't available for {payload.language} yet -- see trace_probe.py for why.")

    visible_args = [tc.args for tc in problem.test_cases if not tc.is_hidden]
    if payload.args not in visible_args:
        raise HTTPException(status_code=400, detail="args must exactly match one of this problem's visible example test cases")

    call_name = function_name_for_language(problem.function_name, payload.language)
    if payload.language == "javascript":
        report = trace_javascript_execution(payload.code, call_name, payload.args, problem.io_transform)
    elif payload.language == "java":
        java_param_types, java_return_type = _java_call_types(problem)
        report = trace_java_execution(payload.code, call_name, payload.args, problem.io_transform, java_param_types, java_return_type)
    else:
        report = trace_python_execution(payload.code, call_name, payload.args, problem.io_transform)
    return TraceResponse(
        supported=report.supported, reason=report.reason, status=report.status, error_message=report.error_message,
        result=report.result, steps=[TraceStepOut(line=s.line, depth=s.depth, locals=s.locals) for s in report.steps],
        truncated=report.truncated, source_lines=report.source_lines,
    )


@router.get("/{slug}/explain", response_model=ExplainResponse)
def explain_last_submission(
    slug: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Turns the most recent submission's *already-computed* diagnosis evidence into a
    plain-language explanation via the local LLM. The model is only allowed to phrase
    facts we hand it -- it is explicitly told not to introduce new claims -- but small
    local models can still misstate a detail, so the response is labeled as generated
    and shown alongside (never instead of) the deterministic evidence list."""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    last_submission = (
        db.query(Submission)
        .filter(Submission.user_id == current_user.id, Submission.problem_id == problem.id, Submission.diagnosis.isnot(None))
        .order_by(Submission.created_at.desc())
        .first()
    )
    if not last_submission or not last_submission.diagnosis:
        raise HTTPException(status_code=404, detail="No diagnosed submission yet -- submit a solution first")

    diag = last_submission.diagnosis
    facts = "\n".join(f"- {e}" for e in diag["evidence"])
    try:
        explanation = llm_generate(
            system_prompt=(
                "You are a concise DSA tutor. Explain the student's result using ONLY the facts listed below. "
                "Do not invent test results, hint counts, or claims not present in the facts. 2-4 short sentences."
            ),
            user_prompt=(
                f"Problem: {problem.title}\nDiagnosed issue: {diag['primary_issue']}\nFacts:\n{facts}\n\n"
                "Explain what likely happened and what to do next."
            ),
        )
    except LocalLLMUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))

    return ExplainResponse(explanation=explanation, grounded_in=diag["evidence"])


@router.post("/{slug}/ask", response_model=AskResponse)
def ask_about_problem(
    slug: str, payload: AskRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    """Free-form Q&A about a problem, answered by the local LLM grounded in the problem's
    own statement/constraints. This is a soft boundary, not a hard one: the system prompt
    asks the model to guide rather than hand over a full solution, but a small local model
    can be talked past that -- same limitation any hint system has."""
    problem = db.query(Problem).filter(Problem.slug == slug).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    try:
        answer = llm_generate(
            system_prompt=(
                "You are a DSA tutor helping a student understand a problem -- not solve it for them. "
                "Guide their thinking (clarify the problem, suggest what to consider) rather than giving full "
                "working code. Keep answers to 3-5 sentences."
            ),
            user_prompt=(
                f"Problem: {problem.title}\n{problem.statement_markdown}\n"
                f"Constraints: {problem.constraints_markdown}\n\nStudent's question: {payload.question}"
            ),
            max_tokens=260,
        )
    except LocalLLMUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))

    return AskResponse(answer=answer)
