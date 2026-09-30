from pydantic import BaseModel


class ConceptBridgeItem(BaseModel):
    domain: str  # "dsa" | "system_design" | "networks"
    key: str
    title: str
    similarity: float


class ConceptBridgeResponse(BaseModel):
    bridges: list[ConceptBridgeItem]


class ConceptBridgePairOut(BaseModel):
    a_domain: str
    a_key: str
    a_title: str
    b_domain: str
    b_key: str
    b_title: str
    similarity: float
