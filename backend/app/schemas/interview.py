from pydantic import BaseModel


class StartInterviewRequest(BaseModel):
    type: str  # dsa | system_design
    problem_slug: str | None = None
    case_slug: str | None = None


class InterviewMessageOut(BaseModel):
    role: str
    stage: str
    content: str


class StartInterviewResponse(BaseModel):
    session_id: str
    stage: str
    messages: list[InterviewMessageOut]


class AnswerRequest(BaseModel):
    content: str


class AnswerResponse(BaseModel):
    stage: str
    finished: bool
    messages: list[InterviewMessageOut]
    commentary: str | None = None


class InterviewReport(BaseModel):
    stages_completed: int
    total_stages: int
    transcript: list[InterviewMessageOut]
    coverage_score: float
    summary: str


class MockLoopStartResponse(BaseModel):
    loop_id: str
    stage: str
    dsa_problem_slug: str
    dsa_problem_title: str
    sd_case_slug: str
    sd_case_title: str
    behavioral_question: str


class MockLoopStateOut(BaseModel):
    loop_id: str
    stage: str
    dsa_problem_slug: str
    dsa_submitted: bool
    dsa_passed: bool | None
    sd_case_slug: str
    sd_submitted: bool
    sd_score: float | None
    behavioral_question: str
    behavioral_submitted: bool


class BehavioralAnswerRequest(BaseModel):
    answer: str


class MockLoopReportOut(BaseModel):
    dsa_problem_title: str
    dsa_passed: bool | None
    dsa_passed_count: int | None
    dsa_total_count: int | None
    sd_case_title: str
    sd_score: float | None
    sd_missing_components: list[str]
    sd_unjustified_components: list[str]
    behavioral_question: str
    behavioral_tier: str | None
    behavioral_coaching_tip: str | None
    behavioral_star_score: float | None
    overall_summary: str
