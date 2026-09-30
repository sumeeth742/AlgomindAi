from datetime import datetime

from pydantic import BaseModel


class ProblemListItem(BaseModel):
    id: str
    slug: str
    title: str
    difficulty: str
    primary_skill_key: str
    concept_difficulty: int
    implementation_difficulty: int
    reasoning_difficulty: int
    pattern_difficulty: int
    solved: bool
    attempted: bool


class TransferChallengeOut(BaseModel):
    available: bool
    problem_slug: str | None = None
    problem_title: str | None = None
    reason: str


class BlindPracticeOut(BaseModel):
    available: bool
    problem_slug: str | None = None
    reason: str


class VisibleTestCase(BaseModel):
    args: list
    expected_output: object
    explanation: str


class ProblemDetail(BaseModel):
    id: str
    slug: str
    title: str
    statement_markdown: str
    difficulty: str
    constraints_markdown: str
    examples: list
    function_name: str
    param_names: list[str]
    starter_code: str
    language: str
    supported_languages: list[str]
    time_limit_ms: int
    expected_complexity: str
    primary_skill_key: str
    visible_test_cases: list[VisibleTestCase]
    # patterns/topics are withheld in "blind" mode by the router, not here


class SubmitRequest(BaseModel):
    code: str
    mode: str = "standard"
    language: str = "python"
    time_to_solve_seconds: float | None = None
    hint_count_used: int = 0


class TestResultOut(BaseModel):
    index: int
    passed: bool
    is_hidden: bool
    input: list | None = None
    expected: object | None = None
    actual: object | None = None
    error: str | None = None


class RunRequest(BaseModel):
    code: str
    language: str = "python"


class RunResponse(BaseModel):
    status: str
    passed_count: int
    total_count: int
    runtime_ms: float
    test_results: list[TestResultOut]


class SubmitResponse(BaseModel):
    submission_id: str
    status: str
    passed_count: int
    total_count: int
    runtime_ms: float
    test_results: list[TestResultOut]
    diagnosis: dict | None = None
    updated_mastery: float | None = None
    repeat_solve_note: str | None = None
    optimization_nudge: str | None = None
    language: str = "python"
    runtime_percentile: float | None = None


class ComplexityCheckRequest(BaseModel):
    code: str
    language: str = "python"


class ComplexitySampleOut(BaseModel):
    size: int
    status: str
    runtime_ms: float | None = None


class ComplexityCheckResponse(BaseModel):
    supported: bool
    reason: str | None = None
    samples: list[ComplexitySampleOut] = []
    estimated_exponent: float | None = None
    estimated_label: str | None = None
    expected_complexity: str = ""
    likely_matches_expected: bool | None = None
    explanation: str = ""


class TraceRequest(BaseModel):
    code: str
    language: str = "python"
    args: list  # must exactly match one of this problem's VISIBLE example test cases


class TraceStepOut(BaseModel):
    line: int
    depth: int
    locals: dict


class TraceResponse(BaseModel):
    supported: bool
    reason: str | None = None
    status: str | None = None
    error_message: str | None = None
    result: object = None
    steps: list[TraceStepOut] = []
    truncated: bool = False
    source_lines: list[str] = []


class SubmissionHistoryItem(BaseModel):
    id: str
    status: str
    language: str
    passed_count: int
    total_count: int
    runtime_ms: float
    created_at: datetime
    code: str


class ExplainResponse(BaseModel):
    explanation: str
    grounded_in: list[str]


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


class ReasoningSubmitRequest(BaseModel):
    declared_pattern: str
    reasoning_text: str = ""


class ReasoningSubmitResponse(BaseModel):
    is_correct_pattern: bool
    correct_pattern: str
    reasoning_quality_score: float
    evidence_matched: list[str]
    missing_evidence: list[str]
    declared_pattern_evidence: list[str]
    feedback: str
    plan_quality_coach: dict | None = None
