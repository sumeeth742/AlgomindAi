from pydantic import BaseModel


class ComicPanelOut(BaseModel):
    speaker: str  # "mira" | "dev"
    text: str


class NetworkLessonOut(BaseModel):
    id: str
    slug: str
    title: str
    level: int
    category: str
    content_markdown: str
    practical_connection: str
    comic_script: list[ComicPanelOut]


class NetworkConceptMapNodeOut(BaseModel):
    slug: str
    title: str
    category: str
    level: int


class NetworkConceptMapOut(BaseModel):
    current: NetworkConceptMapNodeOut
    previous: NetworkConceptMapNodeOut | None
    next: NetworkConceptMapNodeOut | None


class NetworkQuizQuestionOut(BaseModel):
    id: str
    question: str
    options: list[str]


class NetworkQuizAnswerIn(BaseModel):
    question_id: str
    selected_index: int


class NetworkQuizAnswerOut(BaseModel):
    correct: bool
    correct_index: int
    explanation: str
