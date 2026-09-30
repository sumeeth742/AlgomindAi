from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.concept_bridge import ConceptBridgeItem, ConceptBridgePairOut, ConceptBridgeResponse
from app.services.concept_bridge.bridge import get_bridges, get_top_bridges_platform_wide

router = APIRouter(prefix="/concept-bridges", tags=["concept-bridges"])

VALID_DOMAINS = {"dsa", "system_design", "networks"}


@router.get("/{domain}/{key}", response_model=ConceptBridgeResponse)
def get_lesson_bridges(domain: str, key: str, db: Session = Depends(get_db)):
    if domain not in VALID_DOMAINS:
        raise HTTPException(status_code=400, detail=f"domain must be one of {sorted(VALID_DOMAINS)}")
    bridges = get_bridges(db, domain, key)
    return ConceptBridgeResponse(bridges=[ConceptBridgeItem(**b) for b in bridges])


@router.get("", response_model=list[ConceptBridgePairOut])
def get_platform_bridges(db: Session = Depends(get_db)):
    """Whole-platform explorer: the strongest real cross-curriculum lexical
    links found anywhere, for a dedicated browse page rather than one lesson
    at a time."""
    return get_top_bridges_platform_wide(db)
