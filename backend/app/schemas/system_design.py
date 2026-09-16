from pydantic import BaseModel


class ComicPanelOut(BaseModel):
    speaker: str  # "mira" | "dev"
    text: str


class SystemDesignLessonOut(BaseModel):
    id: str
    slug: str
    title: str
    level: int
    category: str
    content_markdown: str
    dsa_connection: str
    comic_script: list[ComicPanelOut]


class SystemDesignCaseOut(BaseModel):
    id: str
    slug: str
    title: str
    difficulty: str
    base_slug: str | None
    scale_tier: str | None
    scale_description: str | None
    description_markdown: str
    functional_requirements: list
    non_functional_requirements: list
    estimation_prompt: str
    editorial_markdown: str


class ArchitectureNode(BaseModel):
    id: str
    type: str  # client | server | database | cache | queue | cdn | load_balancer | object_storage | search


class ArchitectureEdge(BaseModel):
    source: str
    target: str


class SystemDesignAttemptRequest(BaseModel):
    nodes: list[ArchitectureNode]
    edges: list[ArchitectureEdge]
    estimation_answers: dict = {}


class SystemDesignAttemptResponse(BaseModel):
    score: float
    missing_components: list[str]
    unjustified_components: list[str]
    estimation_feedback: dict
    why_questions: list[str]
    scope_coach: dict | None = None


class LessonConceptMapNodeOut(BaseModel):
    slug: str
    title: str
    category: str
    level: int


class LessonConceptMapOut(BaseModel):
    current: LessonConceptMapNodeOut
    previous: LessonConceptMapNodeOut | None
    next: LessonConceptMapNodeOut | None
