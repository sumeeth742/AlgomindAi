from pydantic import BaseModel


class LLDCaseOut(BaseModel):
    id: str
    slug: str
    title: str
    difficulty: str
    description_markdown: str
    functional_requirements: list
    non_functional_requirements: list
    abstraction_hint: str
    editorial_markdown: str


class LLDClassIn(BaseModel):
    name: str
    fields: list[str] = []
    methods: list[str] = []
    extends: str | None = None
    implements: list[str] = []


class LLDAttemptRequest(BaseModel):
    classes: list[LLDClassIn]


class LLDAttemptResponse(BaseModel):
    score: float
    missing_classes: list[str]
    extra_classes: list[str]
    uses_abstraction: bool
    god_classes: list[str]
    why_questions: list[str]
