from pydantic import BaseModel


class SkillOut(BaseModel):
    id: str
    key: str
    name: str
    chapter: str
    level: int
    description: str

    class Config:
        from_attributes = True


class ComicPanelOut(BaseModel):
    speaker: str  # "mira" | "dev"
    text: str


class SkillLessonOut(SkillOut):
    concept_markdown: str
    mnemonic: str
    comic_script: list[ComicPanelOut]


class UserSkillOut(BaseModel):
    skill_key: str
    skill_name: str
    chapter: str
    mastery: float
    confidence: float
    attempts: int
    correct_attempts: int
    pattern_recognition_accuracy: float | None
    transfer_accuracy: float | None


class SkillReadinessOut(BaseModel):
    skill_key: str
    ready: bool
    unmet_prerequisites: list[str]


class ConceptMapNodeOut(BaseModel):
    key: str
    name: str
    chapter: str


class ConceptMapOut(BaseModel):
    current: ConceptMapNodeOut
    prerequisites: list[ConceptMapNodeOut]
    unlocks: list[ConceptMapNodeOut]
